from app.db import db
from app.models.user import User

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.Column(db.String(10), default='python')
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    url_image = db.Column(db.String(255))
    url_github = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User, backref='projects')

    def __init__(self, tags, title, description, url_image, url_github, user_id):
        self.tags = tags
        self.title = title
        self.description = description
        self.url_image = url_image
        self.url_github = url_github
        self.user_id = user_id
