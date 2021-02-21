from app import create_app, db
from app.models import User
from flask_migrate import Migrate, upgrade

app = create_app('default')
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User)

app.run(host='0.0.0.0')

upgrade()
