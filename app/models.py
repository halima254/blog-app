from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from . import login_manager
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id  = db.Column(db.Interger, primary_key=True)
    username = db.Column(db.String(64),index=True,unique=True)
    email = db.Column(db.String(100), index= True, unique=True)
    password_hash = db.Column(db.String(100))
    bio = db.Column(db.String(250))
    profile_pic_path = db.Column(db,String())
    blog = db.relationship('Pitch',backref ='user', lazy='dynamic')
    comment = db.relationship('Comment',backref='user',lazy='dynamic')
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hask(self.password_hash,password)
    
    def __repr__(self):
        return f'User {self.username}'
    
    @login_manager.user_loader
    def load_user(author_id):
        return User.query.get(int(author_id))
    
        
        
    
