from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from server.User import User
from database.db_manager import DB_Manager
from flask_sslify import SSLify

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        db = DB_Manager("database/kundendatenbank.sql", "users")
        db.connect()
        data = db.get_mail_and_name_by_id(user_id)
        role = db.get_role_by_id(user_id)
        db.disconnect()                                     # new
        return User(int(user_id), data[0], data[1], role[0])


    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)


    return app