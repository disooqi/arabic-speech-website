#create DB
# NB! you need to set (export ARABIC_SPEECH_DB_URI="sqlite:///arabic_speech.db") in the .bashrc file in order for this
# to run properly
 from arabic_speech_community import db
from arabic_speech_community.models import User, MGB2Link, Post

 db.create_all()
 
disooqi = User(fullname='Mohamed Eldesouki', email='disooqi@gmail.com', password='123', position='Research Associate',
            affiliation='Qatar Computing Research Associate', department='ALT', address='QCRI/Research Complex/HBKU/QF',
            telephone='974-33542583')

mohamohamed = User(fullname='Mohamed Eldesouki', email='mohamohamed@qf.org.qa', password='123', position='Research Associate',
            affiliation='Qatar Computing Research Associate', department='ALT', address='QCRI/Research Complex/HBKU/QF',
            telephone='974-33542583')

p1 = Post(title='my title', content='my content', user_id=disooqi.id)

db.session.add(disooqi)
db.session.add(mohamohamed)
db.session.commit()
