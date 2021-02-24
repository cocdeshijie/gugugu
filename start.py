from app import create_app, db
from app.models import Group, FileExtension, User, Upload
from flask_migrate import Migrate, upgrade

app = create_app('default')
migrate = Migrate(app, db)


app.run(host='0.0.0.0')

upgrade()
