from app.models import User
from app import db
user = User.query.filter_by(username='cocdeshijie').first()
print(user.username)
