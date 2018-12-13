from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(60), nullable=True)

    position = db.Column(db.String(100), nullable=True)
    affiliation = db.Column(db.String(120), nullable=True)
    
    department = db.Column(db.String(120), nullable=True)
    
    address = db.Column(db.String(200), nullable=True)
    telephone = db.Column(db.String(15), nullable=True)
    

    mgb2links = db.relationship('MGB2link', backref='requester', lazy=True)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}','{self.password}', \
        '{self.position}','{self.affiliation}','{self.department}', \
        '{self.address},{self.telephone}')"


class MGB2link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_requested = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    date_downloaded = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    n_downloads = db.Column(db.Integer, nullable=False, default=0)
      
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"MGB2User('{self.date_requested}', '{self.downloaded}')"
