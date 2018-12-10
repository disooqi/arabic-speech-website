#create DB
from arabic_speech_community import db
from arabic_speech_community.models import User


print (User.query.all())
ahmed = User.query.first()
print (ahmed.password)
'''
User.query.first()
User.query.filter_by(username='ahmed').all()
User.query.filter_by(username='ahmed').first()
User.query.get(1)
'''