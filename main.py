from app import create_app, db
from flask_migrate import Migrate
from app.models.user import User

app = create_app()
migrate = Migrate(app, db) 