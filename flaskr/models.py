from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
#from . import db
from flaskr.db import Base
from sqlalchemy.orm import relationship
from flask_login import UserMixin
#db = SQLAlchemy()

class User(UserMixin, Base):
    __tablename__ = 'user_tb'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    username = Column(
        String,
        unique=True,
        nullable=False
    )
    password = Column(
        String,
        unique=True,
        nullable=False
    )

    def __init__(self, username=None, password=None):
        self.username = username 
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

class Post(Base):
    __tablename__ = 'post'
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    author_id = Column(
        Integer,
        ForeignKey('user_tb.id'),
        nullable=False
    )
    created = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False
    )
    title = Column(
        String,
        nullable=False
    )
    body = Column(
        Text,
        nullable=True
    )
    
    #user = relationship("User", back_populates="post")

    def __init__(self, id, author_id, created, title, body):
         self.id = id
         self.author_id = author_id
         self.created = created
         self.title = title
         self.body = body
    # user = relationship("User", backref=backref("user", uselist=False))
    def __repr__(self):
        #return '<Post {}>'.format(self.author_id)
        return '<User %r>' % (self.author_id)

#User.post = relationship("Post", order_by=post.id, back_populates="user")
