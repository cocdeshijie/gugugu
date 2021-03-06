from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager
import bitmath
import secrets
from datetime import datetime
import os


class SiteSetting(db.Model):
    __tablename__ = 'sitesetting'
    id = db.Column(db.Integer, primary_key=True)
    site_title = db.Column(db.String, default='placeholder')
    site_description = db.Column(db.String, default='placeholder')
    guest_upload = db.Column(db.Boolean, default=True)
    api = db.Column(db.Boolean, default=True)
    default_group_id = db.Column(db.Integer, default=2)
    default_file_location = db.Column(db.String, default='local')
    file_count = db.Column(db.Integer, default=0)


class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    admin = db.Column(db.Boolean, default=False)
    space_limits = db.Column(db.Integer, default=536870912)
    delete = db.Column(db.Boolean, default=True)
    users = db.relationship('User', backref='group')
    extension_setting = db.Column(db.Boolean, default=False)  # True=whitelist, False=blacklist
    extensions = db.Column(db.String, default='')

    @property
    def space_limit(self):
        return 'infinite' if self.space_limits == 0 \
            else bitmath.Byte(bytes=self.space_limits).best_prefix().format("{value:.2f}{unit}")

    @space_limit.setter
    def space_limit(self, bytes):
        self.space_limits = bytes

    @property
    def user_count(self):
        return len(self.users)

    @property
    def extension_list(self):
        return [extension.strip() for extension in self.extensions.split(',')]

    @property
    def extensions_input(self):
        return self.extensions

    @extensions_input.setter
    def extensions_input(self, extensions):
        extensions= [extension.strip() for extension in extensions.split(',')]
        self.extensions = ', '.join(extensions)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    bytes = db.Column(db.Integer, default=0)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), default=2)
    uploads = db.relationship('Upload', backref='user', lazy='dynamic')
    api_key = db.Column(db.String(16), default=secrets.token_urlsafe(16))

    @property
    def group_name(self):
        return Group.query.get(self.group_id).name

    @property
    def upload_count(self):
        return self.uploads.count()

    @property
    def max_space(self):
        return Group.query.get(self.group_id).space_limit

    @property
    def space_used(self):
        return bitmath.Byte(bytes=self.bytes).best_prefix().format("{value:.2f} {unit}")

    @space_used.setter
    def space_used(self, change):
        self.bytes += change

    @property
    def password(self):
        raise AttributeError('Passwords are hashed.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Upload(db.Model):
    __tablename__ = 'uploads'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    original_name = db.Column(db.String)
    name = db.Column(db.String)
    size = db.Column(db.Integer)
    path = db.Column(db.String)
    mime_type = db.Column(db.String)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    secret = db.Column(db.Boolean, default=False) # true = on
    password = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Passwords are hashed.')

    @password.setter
    def password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def put_file(self, file):
        self.mime_type = file.mimetype
        self.original_name = file.filename
        self.name = '{}.{}'.format(secrets.token_hex(8),
                                   file.filename.split('.')[-1])
        self.path = '{}'.format(self.name)
        target = './app/static/files/{}'.format(self.path)
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        file.save(target)
        self.size = os.path.getsize(target)
        return 'Success'




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))