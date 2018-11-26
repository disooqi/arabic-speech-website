from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)

    position = db.Column(db.String(100), nullable=True)
    institution = db.Column(db.String(120), nullable=True)
    # Department (if applicable)
    department = db.Column(db.String(120), nullable=True)
    # Postal Address
    address = db.Column(db.String(200), nullable=True)
    telephone = db.Column(db.String(15), nullable=True)
    fax = db.Column(db.String(15), nullable=True)

    posts = db.relationship('Post', backref='author', lazy=True)
    mgb2links = db.relationship('MGB2link', backref='requester', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class MGB2link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_requested = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_downloaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    n_downloads = db.Column(db.Integer, nullable=False, default=0)
    # Intent for use of the Corpus
    intent = db.Column(db.Text, nullable=True)
    # If You have previously been in contact with the Corpus developers, please list their names:
    corpus_developers = db.Column(db.String(150), nullable=True)
    # Are You willing to contribute to the Corpus for future releases?
    willing_to_contribute = db.Column(db.String(20), nullable=False, default='No')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"MGB2User('{self.date_requested}', '{self.downloaded}')"
