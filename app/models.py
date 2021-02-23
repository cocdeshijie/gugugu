from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
import bitmath



class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String)
    manage_group = db.Column(db.Boolean)
    manage_user = db.Column(db.Boolean)
    space_limit = db.Column(db.Integer, default=536870912)
    users = db.relationship('User', backref='group')
    extension_setting = db.Column(db.Boolean, default=False)  # True=whitelist, False=blacklist
    extensions = db.relationship('FileExtension', backref='extensions')


class FileExtension(db.Model):
    __tablename__ = 'fileextensions'
    id = db.Column(db.Integer, primary_key=True)
    file_extension = db.Column(db.String)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.Integer, default=3)
    space_used = db.Column(db.Integer, default=0)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'))
    uploads = db.relationship('Upload', backref='user')

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


class Upload(db.Model):
    __tablename__ = 'uploads'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    size = db.Column(db.Integer)
    path = db.Column(db.String)
    mime_type = db.Column(db.String)
    date = db.Column(db.Date)
    request_volume = db.Column(db.Integer)
    password = db.Column(db.Boolean)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
