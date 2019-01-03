#create DB
from arabic_speech_community import db
from arabic_speech_community.models import User, MGB2Link


allUsers=User.query.all()
for user in allUsers:
	print (user.fullname, user.email, user.position, user.affiliation,'\n')

'''
print (User.query.all())
ahmed = User.query.first()
print (ahmed)
User.query.first()
User.query.filter_by(username='ahmed').all()
User.query.filter_by(username='ahmed').first()
User.query.get(1)
'''

