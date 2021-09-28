from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id  = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(140), index= True, unique=True)
    password_hash = db.Column(db.String(128))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    blog = db.relationship('Blog',backref ='user', lazy='dynamic')
    comment = db.relationship('Comment',backref='user',lazy='dynamic')
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def __repr__(self):
        return f'User {self.username}'
    
    @login_manager.user_loader
    def load_user(author_id):
        return User.query.get(int(author_id))
    
    
class Blog(db.Model):    
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    content = db.Column(db.String)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment = db.relationship('Comment', backref='blog_id', lazy='dynamic')
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()
        
    # @classmethod
    # def get_blogs(cls):
    #     return blogs
    
    @classmethod 
    def get_blog(self):
        blog = Blog.query.all()
        return blog
        
class Comment(db.Model):
    __tablename__ = 'comments' 
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog = db.Column(db.Integer, db.ForeignKey('blogs.id'))
    
    def save_comments(self):
        db.session.add(self)
        db.session.commit()
        
    @classmethod
    def get_comments(cls, blog):
        comments = Comment.query.filter_by(blog_id = blog).all()
        return comments  
                  
    
