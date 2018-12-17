import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message


app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = "arabicspeechinfo@gmail.com"
app.config['MAIL_PASSWORD'] = "ArabicSpeech123"
app.config['MAIL_DEFAULT_SENDER'] = 'arabicspeechinfo@gmail.com'
info_mail = Mail(app)





def send_confirm_email(email):
    
    msg = Message('Email Confirmation - arabicspeech.org',  recipients=[email])
    msg.body = f'''A user on "arabicspeech.org" has created an account using this email address.
    
To confirm this email address, go to: 

If you did not sign up for this site, you can ignore this message.
'''
    info_mail.send(msg)

@app.route('/')
@app.route('/home')
def home():
    send_confirm_email ("ahmaksod@gmail.com")
    return "hello"




if __name__ == '__main__' :
	app.run (debug=True,host='0.0.0.0')
	
	
