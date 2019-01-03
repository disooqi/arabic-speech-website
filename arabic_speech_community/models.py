from datetime import datetime
from . import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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

    '''
    This is to define users privialges 
    0 not allowed to login 
    1 can loging and download corpus
    2 
    100 can edit the website and submit blog
    1000 admin
    '''
    rank = db.Column(db.Integer, nullable=False, default=0)

    posts = db.relationship('Post', backref='author', lazy=True)
    mgb2_downloads = db.relationship('MGB2Link', backref='downloader', lazy=True, uselist=True)

    def get_reset_token(self, expires_secs=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_secs)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.fullname}', '{self.email}','{self.password}', \
        '{self.position}','{self.affiliation}','{self.department}', \
        '{self.address},{self.telephone}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class MGB2Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mgb2_part = db.Column(db.String(5), nullable=False)
    date_requested = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_date_downloaded = db.Column(db.DateTime, nullable=True)
    n_downloads = db.Column(db.Integer, nullable=False, default=0)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # 'user' here is the table name

    def get_MGB2_token(self, expires_secs=60*60*24*365):
        s = Serializer(app.config['SECRET_KEY'], expires_secs)
        return s.dumps({'link_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_MGB2_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            link_id = s.loads(token)['link_id']
        except:
            return None
        return MGB2Link.query.get(link_id)
      
    def __repr__(self):
        return f"MGB2Link('{self.mgb2_part}', '{self.date_requested}', , '{self.n_downloads}')"
