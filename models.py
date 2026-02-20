from sqlalchemy import Integer, String, ForeignKey,DateTime,Boolean
from flask_login import UserMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import db
from datetime import datetime


class Notifications(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String,nullable=False)
    message:Mapped[str] = mapped_column(String,nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean,default=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    receiver_id: Mapped[int] = mapped_column(Integer,ForeignKey("user.id"))
    sender_id: Mapped[int] = mapped_column(Integer,ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(Integer,ForeignKey("blog_post.id"),nullable=True)
    comment_id: Mapped[int] = mapped_column(Integer,ForeignKey("comments.id"),nullable=True)

    receiver = relationship("User",back_populates="notifications",foreign_keys=[receiver_id])
    sender = relationship("User",back_populates="sent_notifications",foreign_keys=[sender_id])
    post = relationship("BlogPost",back_populates="notifications")
    comment = relationship("Comments",back_populates="notifications")


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    name: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean,default=False)
    is_restricted: Mapped[bool] = mapped_column(Boolean,default=False)

    posts = relationship("BlogPost",back_populates="author",cascade="all, delete-orphan")
    comments = relationship("Comments",back_populates="author",cascade="all, delete-orphan")
    likes = relationship("Likes",back_populates="author",cascade="all, delete-orphan")
    notifications = relationship("Notifications",back_populates="receiver",cascade="all, delete-orphan",foreign_keys=[Notifications.receiver_id])
    sent_notifications = relationship("Notifications",back_populates="sender",cascade="all, delete-orphan",foreign_keys=[Notifications.sender_id])

    @property
    def is_super_admin(self):
        return self.id ==1

    @property
    def admin_privileges(self):
        return self.is_admin or self.is_super_admin


class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer,ForeignKey("user.id"))
    title: Mapped[str] = mapped_column(String,nullable=False,unique=True)
    subtitle: Mapped[str] = mapped_column(String,nullable=False)
    date: Mapped[str] = mapped_column(String,nullable=False)
    body: Mapped[str] = mapped_column(String,nullable=False)
    img_url: Mapped[str] = mapped_column(String,nullable=False)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comments", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Likes",back_populates="post",cascade="all, delete-orphan")
    notifications = relationship("Notifications",back_populates="post",cascade="all, delete-orphan")



class Comments(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer,ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("blog_post.id"))
    text: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow)
    edited = db.Column(db.Boolean, default=False)

    author = relationship("User",back_populates="comments")
    post = relationship("BlogPost",back_populates="comments")
    likes = relationship("Likes",back_populates="comment",cascade="all, delete-orphan")
    notifications = relationship("Notifications",back_populates="comment",cascade="all, delete-orphan")


class Likes(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer,ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(Integer,ForeignKey("blog_post.id"),nullable=True)
    comment_id: Mapped[int] = mapped_column(Integer, ForeignKey("comments.id"), nullable=True)

    author = relationship("User",back_populates="likes")
    post = relationship("BlogPost",back_populates="likes")
    comment = relationship("Comments",back_populates="likes")



