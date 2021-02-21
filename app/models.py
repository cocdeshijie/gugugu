from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, default=3)

    @property
    def password(self):
        raise AttributeError('Passwords are hashed.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_role(self):
        roles = {1: 'Owner', 2: 'Moderator', 3: 'User', 4: 'Guest'}
        return roles[self.role]





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
