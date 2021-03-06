from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)

    with app.app_context():
        db.create_all()
        # create default admin user
        from .models import Group, User
        if Group.query.first() is None:
            group = Group(name='Admin',
                          admin=True,
                          space_limits=0,
                          delete=False)
            group2 = Group(name='Default Group')
            db.session.add_all([group, group2])
            db.session.commit()
            user = User(username='admin',
                        email='admin@admin.admin',
                        password='123456',
                        group_id=group.id)
            db.session.add(user)
            db.session.commit()
        # create site setting
        from.models import SiteSetting
        if SiteSetting.query.first() is None:
            setting = SiteSetting()
            db.session.add(setting)
            db.session.commit()

    login_manager.init_app(app)
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app

