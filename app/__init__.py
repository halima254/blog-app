from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_options
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask_mail import Mail

mail = Mail()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)

def create_app(config_name):
    
    # Initializing application
    app = Flask(__name__)
    
#creating the app configurations
    app.config.from_object(config_options[config_name])
#Registering the Blueprint
    from .main import main as main_blueprint
#Initializing Flask Extensionsin_blueprint
    app.register_blueprint(main_blueprint)
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint,url_prefix = '/auth') 
    mail.init_app(app) 
   
#setting config
    # from .request import configure_request
    # configure_r
    # request(app)    

#configure UploadSet
    configure_uploads(app,photos)
#will add the views and the forms
  
    from .main import views,error    
    return app
    
