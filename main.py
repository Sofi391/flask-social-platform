from flask import Flask,render_template,request,url_for,redirect,flash,abort,session,jsonify
from flask_bootstrap import Bootstrap5
from sqlalchemy.testing.pickleable import User
from werkzeug.utils import redirect
from flask_ckeditor import CKEditor
from flask_login import current_user, login_user, logout_user, login_required, LoginManager
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from flask_gravatar import Gravatar
from datetime import datetime,timedelta
import smtplib
import random
import os
from dotenv import load_dotenv
from forms import CreatePostForm,RegisterForm,LoginForm,CommentForm,EmailVerify,PassReset
from database import db
from models import User,BlogPost,Comments,Likes,Notifications


load_dotenv()

my_email = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASSWORD')


# response = requests.get("https://api.npoint.io/94017f599a3b143c553c")
# response.raise_for_status()
# data = response.json()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
bootstrap = Bootstrap5(app)

app.config['CKEDITOR_PKG_TYPE'] = 'full'
ckeditor = CKEditor(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
db.init_app(app)

# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     print("✅ Database has been reset successfully!")

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    flash("You need to login/register first.")
    return redirect(url_for("login"))


def email_notification(receiver,sub,msg):
    with smtplib.SMTP(os.getenv('EMAIL_HOST')) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=receiver,
                            msg=f"Subject: {sub}\r\n From: {my_email}\n\n"
                                f"{msg}")


def create_notifications(type,message,receiver_id,sender_id,post_id=None,comment_id=None,is_admin_message=None):
    if not is_admin_message:
        existing = Notifications.query.filter_by(
            type=type,
            message=message,
            receiver_id=receiver_id,
            sender_id=sender_id,
            post_id=post_id,
            comment_id=comment_id
        ).first()
        if existing:
            return

    new_notification = Notifications(
        type=type,
        message=message,
        receiver_id=receiver_id,
        sender_id=sender_id,
        post_id=post_id,
        comment_id=comment_id
    )
    db.session.add(new_notification)
    db.session.flush()



def admin_only (fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(403)
        elif not current_user.admin_privileges:
            return abort(403)
        return fun(*args, **kwargs)
    return wrapper

def super_admin_only(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_super_admin:
            abort(403)
        return fun(*args, **kwargs)
    return wrapper


# with app.app_context():
#     user = User.query.get(1)
#     if user:
#         user.is_admin = True
#         db.session.add(user)
#         db.session.commit()


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email =form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered, login instead.')
            return redirect(url_for('login'))
        password_hash = generate_password_hash(form.password.data,method='pbkdf2:sha256',salt_length=8)
        new_user = User(email=form.email.data,
                        password = password_hash,
                        name=form.name.data,
                        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        create_notifications(
            "Welcome",
            f"Hello {new_user.name},\n\nWelcome to our platform! We're excited to have you on board. Explore the site, engage with posts, and enjoy your experience.\n\nBest regards,\nThe Team",
            receiver_id=new_user.id,
            sender_id=1,
        )
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("register.html",form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash("Email doesn't exist, please register first.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password,form.password.data):
            flash("Password doesn't match")
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home'))
    return render_template("login.html",form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/')
def home():
    blog_ids = [ids.id for ids in BlogPost.query.order_by(BlogPost.date.desc()).all()]
    unread_count = Notifications.query.filter_by(receiver_id=current_user.id,is_read=False).count() if current_user.is_authenticated else 0
    if request.args.get("refresh") == "1":
        random.shuffle(blog_ids)
        session["ordered_post"] = blog_ids
        return redirect(url_for("home"))
    elif "ordered_post" not in session:
        random.shuffle(blog_ids)
        session["ordered_post"] = blog_ids
    ordered_id = session["ordered_post"][:5]
    blogs = BlogPost.query.filter(BlogPost.id.in_(ordered_id)).all()
    blogs.sort(key=lambda x: ordered_id.index(x.id))

    return render_template("index.html",blogs=blogs,home=True,unread_count=unread_count)

@app.route('/load_posts')
def load_posts():
    offset = int(request.args.get('offset',0))
    limit = int(request.args.get('limit',5))
    loaded_posts = session["ordered_post"][offset:limit+offset]
    blogs = BlogPost.query.filter(BlogPost.id.in_(loaded_posts)).all()
    blogs.sort(key=lambda x: loaded_posts.index(x.id))
    if blogs:
        return render_template("loaded_pages.html",blogs=blogs)
    return ""


@app.route('/about')
def about():
    return render_template("about.html")



@app.route('/contact',methods=['GET','POST'])
def contact():
    if request.method == "POST":
        name = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        message = request.form['message']
        try:
            with smtplib.SMTP(os.getenv('EMAIL_HOST'),int(os.getenv('EMAIL_PORT'))) as connection:
                connection.starttls()
                connection.login(user=my_email,password=password)
                connection.sendmail(from_addr=f"{my_email}",
                                    to_addrs=my_email,
                                    msg=f"Subject: Contact form submission\r\n From: {email}\n\n"
                                        f"Username: {name}\nPhone_number: {phone}\nMessage: {message}",)
        except Exception as e:
            print(e)
        receiver = current_user.email
        sub = "We Received Your Message"
        msg = f"""Hello {current_user.name},

Thank you for reaching out to us through our contact form. We've received your message:

"{message}"

Our team will review it and get back to you as soon as possible. 
If you need urgent assistance, feel free to reply to this email.

Best regards,  
The Team"""
        email_notification(receiver, sub, msg)
        return render_template("contact.html",msg_sent=True)
    else:
        user_name = None
        email = None
        if current_user.is_authenticated:
            user_name = current_user.name
            email = current_user.email
        return render_template("contact.html",msg_sent=False,username=user_name,email=email)



@app.route('/my_posts/<int:user_id>')
@login_required
def my_posts(user_id):
    # user = User.query.get(user_id)
    user = User.query.get(user_id)
    posts = BlogPost.query.filter_by(author_id=user_id).order_by(BlogPost.date.desc()).all()
    return render_template("my_posts.html", posts=posts,user=user)



@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post_page(id):
    edited = request.args.get('edited', default=0, type=int)
    form = CommentForm()
    post = BlogPost.query.get_or_404(id)

    if form.validate_on_submit():
        if current_user.is_authenticated and not current_user.is_restricted:
            new_comment = Comments(
                text=form.comment.data,
                author=current_user,
                post=post
            )
            db.session.add(new_comment)
            if post.author.id != current_user.id:
                create_notifications(
                    "Like",
                    f'{current_user.name} commented on your post saying "{new_comment.text}".',
                    receiver_id=post.author.id,
                    sender_id=current_user.id,
                    comment_id=new_comment.id,
                )
            db.session.commit()

            # Handle AJAX
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                html = render_template("single_comment.html", comment=new_comment, current_user=current_user)
                return jsonify(success=True, html=html)

        else:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return jsonify(success=False, message="You must log in first.")
            flash("You need to login or you may have been restricted.")
            return redirect(url_for('login'))

    return render_template("post.html", post=post, form=form, edited=edited)


@app.route('/delete_comment/<int:comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comments.query.get_or_404(comment_id)
    if (current_user.id == comment.author.id) or (current_user.is_admin) or (current_user.id == comment.post.author.id):
        post_id = comment.post.id
        db.session.delete(comment)
        db.session.commit()
        return redirect(url_for('post_page',id=post_id))
    return redirect(url_for('post_page',id=comment.post.id))


@app.route('/edit_comment/<int:comment_id>',methods=['GET','POST'])
@login_required
def edit_comment(comment_id):
    comment = Comments.query.get_or_404(comment_id)
    if request.method == "POST":
        if current_user.id == comment.author.id:
            comment.text = request.form['comment']
            comment.edited = True
            db.session.commit()
            return redirect(url_for('post_page',id=comment.post.id))
        else:
            return abort(403)
    return redirect(url_for('post_page',id=comment.post.id,edited=comment.id))


@app.route('/new_post',methods=['GET','POST'])
@login_required
def new_post():
    forms = CreatePostForm()
    if forms.validate_on_submit():
        if current_user.is_restricted:
            flash("You have been temporarily restricted, you can't make posts.")
            return redirect(url_for('home'))
        new = BlogPost(title=forms.title.data,
                       subtitle=forms.subtitle.data,
                       date = datetime.now().strftime("%B %d, %Y"),
                       body = forms.body.data,
                       author = current_user,
                       img_url = forms.img.data
                       )
        db.session.add(new)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html",forms=forms)


@app.route('/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    post = BlogPost.query.get_or_404(id)
    forms = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        body=post.body,
        img=post.img_url
    )
    if forms.validate_on_submit():
        post.title = forms.title.data
        post.subtitle = forms.subtitle.data
        post.body = forms.body.data
        post.img_url = forms.img.data
        db.session.commit()
        return redirect(url_for("post_page",id=post.id))
    return render_template("make-post.html",forms=forms,edit=True)



@app.route("/delete/<int:id>")
@login_required
def delete_post(id):
    blog = BlogPost.query.get_or_404(id)
    author_id = blog.author.id
    db.session.delete(blog)
    db.session.commit()
    from_page = request.args.get('from')
    if from_page:
        return redirect(url_for("home"))
    return redirect(url_for("my_posts",user_id=author_id))


@app.route("/admin_dashboard")
@admin_only
def admin_dashboard():
    if current_user.is_restricted:
        flash("You have been temporarily restricted from accessing the admin_dashboard.")
        return redirect(url_for('home'))
    users = User.query.all()
    return render_template("admin_dash.html",users=users)


@app.route("/promote/<int:user_id>")
@super_admin_only
def promote(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = True
    create_notifications(
        "Promotion",
        f"Hello {user.name}, your account has been promoted to a higher role with additional privileges.",
        receiver_id=user.id,
        sender_id=current_user.id,
        is_admin_message = True
    )
    db.session.commit()
    receiver=user.email
    sub="You've Been Promoted!"
    msg=f"""Hello {user.name},
    
Congratulations! Your account has been promoted to a higher role on our platform.
You now have additional privileges and access to new features. Please use them responsibly and continue contributing positively to the community.

Best regards,  
The Team"""
    email_notification(receiver, sub, msg)
    return redirect(url_for("admin_dashboard"))


@app.route("/demote/<int:user_id>")
@super_admin_only
def demote(user_id):
    user = User.query.get_or_404(user_id)
    user.is_admin = False
    create_notifications(
        "Demotion",
        f"Hello {user.name}, your account role has been updated and some previous privileges may no longer be available.",
        receiver_id=user.id,
        sender_id=current_user.id,
        is_admin_message=True
    )
    db.session.commit()
    receiver = user.email
    sub = "Your Account Role Has Been Updated"
    msg = f"""Hello {user.name},

We wanted to let you know that your account role has been changed.
Some of your previous privileges may no longer be available. If you believe this change was made in error, please contact us through the contact page.

Best regards,  
The Team"""
    email_notification(receiver, sub, msg)
    return redirect(url_for("admin_dashboard"))


@app.route("/remove_user/<int:user_id>")
@admin_only
def remove_user(user_id):
    user = User.query.get_or_404(user_id)
    receiver = user.email
    sub = "Your Account Has Been Deleted"
    msg = f"""Hello {user.name},

We’re reaching out to confirm that your account has been permanently deleted from our system.

All your posts, comments, and associated data have been removed as part of this process.  
We’re sorry to see you go — if you’d like to return, you’re always welcome to create a new account in the future.

Best regards,  
The Team"""
    if not user.is_admin:
        db.session.delete(user)
        create_notifications(
            "Account Deleted",
            f"Hello {user.name}, your account has been permanently deleted from our system.",
            receiver_id=user.id,
            sender_id=current_user.id,
            is_admin_message=True
        )
        db.session.commit()
        email_notification(receiver, sub, msg)
        return redirect(url_for("admin_dashboard"))
    elif user.is_super_admin:
        return redirect(url_for("admin_dashboard"))
    else:
        if current_user.is_super_admin:
            db.session.delete(user)
            create_notifications(
                "Account Deleted",
                f"Hello {user.name}, your account has been permanently deleted from our system.",
                receiver_id=user.id,
                sender_id=current_user.id,
                is_admin_message=True
            )
            db.session.commit()
            email_notification(receiver, sub, msg)
            return redirect(url_for("admin_dashboard"))
        flash("You can not remove admins!!")
        return redirect(url_for("admin_dashboard"))


@app.route("/restrict_user/<int:user_id>")
@admin_only
def restrict_user(user_id):
    user = User.query.get_or_404(user_id)
    receiver = user.email
    sub = "Your Account Has Been Restricted"
    msg = f"""Hello {user.name},

Your account has been temporarily restricted due to policy violations or unusual activity.

You won't be able to access certain features until this restriction is lifted. If you think this was a mistake, please reach out to us through the contact page.

Thank you for your understanding,  
The Team"""
    if not user.is_admin:
        user.is_restricted = True
        create_notifications(
            "Restriction",
            f"Hello {user.name}, your account has been temporarily restricted due to a policy violation.",
            receiver_id=user.id,
            sender_id=current_user.id,
            is_admin_message=True
        )
        db.session.commit()
        email_notification(receiver, sub, msg)
        return redirect(url_for("admin_dashboard"))
    else:
        if current_user.is_super_admin:
            user.is_restricted = True
            create_notifications(
                "Restriction",
                f"Hello {user.name}, your account has been temporarily restricted due to a policy violation.",
                receiver_id=user.id,
                sender_id=current_user.id,
                is_admin_message=True
            )
            db.session.commit()
            email_notification(receiver, sub, msg)
            return redirect(url_for("admin_dashboard"))
        flash("You can not restrict admins!!")
        return redirect(url_for("admin_dashboard"))


@app.route("/unrestrict_user/<int:user_id>")
@admin_only
def unrestrict_user(user_id):
    user = User.query.get_or_404(user_id)
    receiver = user.email
    sub = "Your Account Access Has Been Restored"
    msg = f"""Hello {user.name},

Good news! Your account restriction has been lifted, and you now have full access to your account again.

Thank you for your patience and understanding.

Best regards, 
The Team"""
    if not user.is_admin:
        user.is_restricted = False
        create_notifications(
            "Restriction Lifted",
            f"Hello {user.name}, your account restrictions have been removed. You now have full access to all features again.",
            receiver_id=user.id,
            sender_id=current_user.id,
            is_admin_message=True
        )
        db.session.commit()
        email_notification(receiver, sub, msg)
        return redirect(url_for("admin_dashboard"))
    else:
        if current_user.is_super_admin:
            user.is_restricted = False
            create_notifications(
                "Restriction Lifted",
                f"Hello {user.name}, your account restrictions have been removed. You now have full access to all features again.",
                receiver_id=user.id,
                sender_id=current_user.id,
                is_admin_message=True
            )
            db.session.commit()
            email_notification(receiver, sub, msg)
            return redirect(url_for("admin_dashboard"))
        flash("You can not unrestrict admins!!")
        return redirect(url_for("admin_dashboard"))

@app.route("/post_like/<int:post_id>",methods=['POST'])
@login_required
def post_like(post_id):
    post = BlogPost.query.get_or_404(post_id)
    existing_like = Likes.query.filter_by(author_id=current_user.id, post_id=post.id).first()
    if existing_like:
        db.session.delete(existing_like)
        notification = Notifications.query.filter_by(receiver_id=post.author.id,sender_id=current_user.id,post_id=post.id).first()
        if notification:
            db.session.delete(notification)
        db.session.commit()
        liked=False
    else:
        new_like = Likes(author_id=current_user.id, post_id=post.id)
        db.session.add(new_like)
        if post.author.id != current_user.id:
            create_notifications(
                "Like",
                f"{current_user.name} liked your post.",
                receiver_id=post.author.id,
                sender_id=current_user.id,
                post_id=post_id
            )
        db.session.commit()
        liked=True

    if request.headers.get("X-Requested-With")=="XMLHttpRequest":
        return jsonify({
            "liked": liked,
            "likes_count": len(post.likes)
        })
    return redirect(request.referrer)


@app.route("/like_comment/<int:comment_id>", methods=['POST'])
@login_required
def like_comment(comment_id):
    try:
        comment = Comments.query.get_or_404(comment_id)
        existing_like = Likes.query.filter_by(author_id=current_user.id, comment_id=comment.id).first()

        if existing_like:
            # Unlike the comment
            db.session.delete(existing_like)
            # Remove notification if exists
            notification = Notifications.query.filter_by(
                receiver_id=comment.author.id,
                sender_id=current_user.id,
                comment_id=comment_id,
                type="Like"
            ).first()
            if notification:
                db.session.delete(notification)
            liked = False
        else:
            # Like the comment
            new_like = Likes(author_id=current_user.id, comment_id=comment.id)
            db.session.add(new_like)
            # Create notification if not liking own comment
            if comment.author.id != current_user.id:
                create_notifications(
                    "Like",
                    f"{current_user.name} liked your comment.",
                    receiver_id=comment.author.id,
                    sender_id=current_user.id,
                    comment_id=comment_id
                )
            liked = True

        db.session.commit()

        # Refresh the comment to get updated likes count
        db.session.refresh(comment)
        likes_count = len(comment.likes)

        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({
                "liked": liked,
                "likes_count": likes_count,
                "success": True
            })
        return redirect(request.referrer or url_for('post_page', id=comment.post.id))

    except Exception as e:
        db.session.rollback()
        print(f"Error in like_comment: {str(e)}")
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return jsonify({
                "error": "Failed to process like",
                "success": False
            }), 500
        return redirect(request.referrer or url_for('index'))

@app.route("/search")
def search():
    query = request.args.get("q","").strip()
    post_query = BlogPost.query
    if query:
        post_query = post_query.join(User).filter(db.or_(
            db.func.concat(BlogPost.title, " ", User.name).ilike(f"%{query}%"),
            db.func.concat(BlogPost.title,User.name).ilike(f"%{query}%"),
            db.func.concat(User.name, " ", BlogPost.title).ilike(f"%{query}%"),
            db.func.concat(User.name,BlogPost.title).ilike(f"%{query}%")
        )
        )
    search_result = (post_query.order_by(BlogPost.date.desc()).all())
    found = len(search_result)
    return render_template("search_posts.html",search_results=search_result,found=found)

@app.route("/notifications")
@login_required
def notifications():
    show_notifications = Notifications.query.filter_by(receiver_id=current_user.id).order_by(Notifications.timestamp.desc()).all()
    unread_notis = [unread for unread in show_notifications if not unread.is_read]
    for make_read in unread_notis:
        make_read.is_read = True
    db.session.commit()
    return render_template("notifications.html",show_notifications=show_notifications)


@app.route("/forget_password",methods=["GET","POST"])
def forget_password():
    reset_pass = EmailVerify()
    if reset_pass.validate_on_submit():
        user = User.query.filter_by(email=reset_pass.email_address.data).first()
        if user:
            verification_code = random.randint(10000, 99999)

            session.permanent = True  # ensures we can use permanent_session_lifetime
            app.permanent_session_lifetime = timedelta(minutes=3)

            session['password_reset_code'] = verification_code
            session['password_reset_user'] = user.id
            session['password_reset_time'] = datetime.utcnow().timestamp()

            try:
                with smtplib.SMTP(os.getenv('EMAIL_HOST'), int(os.getenv('EMAIL_PORT'))) as connection:
                    connection.starttls()
                    connection.login(user=my_email, password=password)
                    subject = "Password Reset Request"
                    body = (
                        f"Hello {user.name},\n\n"
                        f"You requested to reset your password. "
                        f"Please use the following verification code to proceed:\n\n"
                        f"Verification Code: {verification_code}\n\n"
                        f"This code is valid for 3 minutes.\n\n"
                        "If you did not request a password reset, please ignore this email.\n\n"
                        "Best regards,\n"
                        "The Team"
                    )
                    message = f"Subject: {subject}\nFrom: {my_email}\nTo: {user.email}\n\n{body}"
                    connection.sendmail(my_email, user.email, message)
            except Exception as e:
                flash("Failed to send email. Please try again later.", "danger")
                print("Email error:", e)
                return redirect(url_for('forget_password'))

            return redirect(url_for('verify'))

        else:
            flash("No account found with that email.", "warning")

    return render_template("forget_password.html", reset_pass=reset_pass)


@app.route("/verification",methods=["GET","POST"])
def verify():
    if request.method == "POST":
        # Get digits from form and join them
        code_entered = "".join([
            request.form.get("digit1", ""),
            request.form.get("digit2", ""),
            request.form.get("digit3", ""),
            request.form.get("digit4", ""),
            request.form.get("digit5", "")
        ])

        # Get stored code and timestamp
        verification_code = str(session.get("password_reset_code"))
        code_time = session.get("password_reset_time")
        current_time = datetime.utcnow().timestamp()

        # Check if code exists
        if not verification_code or not code_time:
            flash("No verification code found. Please request a new one.", "danger")
            return redirect(url_for("forget_password"))

        # Check if code expired (3 minutes)
        if current_time - code_time > 180:
            flash("Verification code expired. Please request a new one.", "warning")
            session.pop("password_reset_code", None)
            session.pop("password_reset_time", None)
            return redirect(url_for("forget_password"))

        # Check if code matches
        if code_entered == verification_code:
            return redirect(url_for("reset_password"))
        else:
            flash("Incorrect code. Please try again.", "danger")
            return redirect(url_for("verify"))
    return render_template("verify_reset.html")


@app.route("/password_reset",methods=["GET","POST"])
def reset_password():
    reset_password = PassReset()
    user_id = session.get("password_reset_user")
    if not user_id:
        flash("Session expired please try again.")
        return redirect(url_for("forget_password"))
    user = User.query.filter_by(id=user_id).first()
    receiver = user.email
    sub = "Your Password Has Been Reset Successfully"
    msg = f"""Hello {user.name},

Your password has been successfully reset. You can now log in to your account using your new password.

If you did not perform this action, please contact our support team immediately.

Thank you for keeping your account secure.

Best regards,
The Team
"""
    if reset_password.validate_on_submit():
        if user:
            password_hash = generate_password_hash(reset_password.confirm_password.data, method='pbkdf2:sha256', salt_length=8)
            user.password = password_hash
            create_notifications(
                "Password Reset Successful",
                f"Hello {user.name}, your password has been successfully reset. You can now log in and access all features.",
                receiver_id=user.id,
                sender_id=1,
                is_admin_message=True
            )
            db.session.commit()
            email_notification(receiver, sub, msg)
            session.pop("password_reset_user", None)
            session.pop("password_reset_code", None)
            session.pop("password_reset_time", None)
            flash("Your password has been reset successfully!", "success")
            return redirect(url_for("login"))
        else:
            flash("User not found.", "danger")
    return render_template("reset_password.html",reset_pass=reset_password)





if __name__ == '__main__':
    app.run(debug=True)

