import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
app.config['SECRET_KEY'] = '0447c95c364a0ae6200b1eee656c9053'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# Mail server
# Mail port
# whither to use TLS (Port: 465 (SSL) or 587 (TLS))
# username and password for that server
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'                            # SMTP Host
app.config['MAIL_PORT'] = 465                                                # SMTP Port
app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USE_TLS'] = True
# https://serverfault.com/questions/413397/how-to-set-environment-variable-in-systemd-service
# https://askubuntu.com/questions/1071415/passing-environment-variables-to-systemd-service
app.config['MAIL_USERNAME'] = os.environ.get('ARABIC_SPEECH_EMAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('ARABIC_SPEECH_EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'info@arabicspeech.org'
info_mail = Mail(app)


from . import routes