from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,BooleanField
from wtforms.validators import DataRequired, URL, Email,Length,EqualTo
from flask_ckeditor import CKEditorField


# WTForm for creating a blog post
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    img = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# TODO: Create a RegisterForm to register new users
class RegisterForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"class": "form-control form-control-lg mb-3 shadow-sm rounded-pill",
                   "placeholder": "Enter your email"}
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8)],
        render_kw={"class": "form-control form-control-lg mb-3 shadow-sm rounded-pill",
                   "placeholder": "Enter your password"}
    )
    name = StringField(
        "Name",
        validators=[DataRequired()],
        render_kw={"class": "form-control form-control-lg mb-3 shadow-sm rounded-pill",
                   "placeholder": "Enter your full name"}
    )
    agree = BooleanField("I agree to the terms and conditions", validators=[DataRequired()])
    submit = SubmitField("Register", render_kw={"class": "btn btn-gradient btn-lg w-100 rounded-pill shadow mt-4 btn-hover"})


# TODO: Create a LoginForm to login existing users

class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={
            "placeholder": "Enter your email",
            "class": "form-control form-control-lg shadow-sm rounded-pill"
        }
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8)],
        render_kw={
            "placeholder": "Enter your password",
            "class": "form-control form-control-lg shadow-sm rounded-pill"
        }
    )
    submit = SubmitField(
        "Login",
        render_kw={"class": "btn btn-gradient btn-lg w-100 rounded-pill shadow mt-3"}
    )
# TODO: Create a CommentForm so users can leave comments below posts
class CommentForm(FlaskForm):
    comment = StringField("",validators=[DataRequired(),Length(max=500)],render_kw={"placeholder":"Add a comment here..."})
    submit = SubmitField("Comment", render_kw={"class": "btn btn-primary btn-circle btn-sm rounded-circle"})

class EmailVerify(FlaskForm):
    email_address = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={
            "class": "form-control form-control-lg shadow-sm rounded-3",
            "placeholder": "Enter your email"
        }
    )
    submit = SubmitField(
        "Verify",
        render_kw={
            "class": "btn btn-primary w-100 py-2",
        }
    )

class PassReset(FlaskForm):
    new_password = PasswordField(
        "New password",
        validators=[DataRequired(), Length(min=8, message="Password must be at least 8 characters")]
    )
    confirm_password = PasswordField(
        "Confirm password",
        validators=[DataRequired(), EqualTo("new_password", message="Passwords must match")]
    )
    submit = SubmitField("Reset")
