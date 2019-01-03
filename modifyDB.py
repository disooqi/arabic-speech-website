'''
This is a quick example to show you how to mody the values in the DB
To add or changee something in the scheme go to .....py
'''
from arabic_speech_community import db
from arabic_speech_community.models import User, MGB2Link


allUsers=User.query.all()
for _user in allUsers:
	_user.rank=1000 if _user.email in ["amali@hbku.edu.qa", "disooqi@gmail.com"] else 1 


db.session.commit()

for _user in allUsers:
	print (_user.fullname,	 _user.email, _user.position, _user.affiliation, _user.rank, '\n')
