from flask import Flask
from .config import Config
from .extensions import db, login_manager


def create_database(app):
    with app.app_context():
        from .models import User, Trek, Booking
        db.create_all()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) 
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    db.init_app(app)
    
    from .routes.auth import auth_bp
    from .routes.admin import admin_bp
    from .routes.staff import staff_bp
    from .routes.user import user_bp
    from .routes.home import home_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(staff_bp, url_prefix="/staff")
    app.register_blueprint(user_bp, url_prefix="/user")
    from . import auth_loader
    
    create_database(app)
              
    return app