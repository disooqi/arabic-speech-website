#create DB
from arabic_speech_community import db
from arabic_speech_community.models import User, MGB2Link


allUsers=User.query.all()
for user in allUsers:
	print (user.fullname, user.email, user.position, user.affiliation, user.rank, '\n')

'''
print (User.query.all())
ahmed = User.query.first()
print (ahmed)
User.query.first()
User.query.filter_by(username='ahmed').all()
User.query.filter_by(username='ahmed').first()
User.query.get(1)
'''

# Number of link requested for all three train, dev and test
dwns = MGB2Link.query.all()
n_link_created = len(dwns)

# Number of dev link requested
devs = MGB2Link.query.filter_by(mgb2_part='dev').all()
n_dev_requested = len(devs)


# Number of link requested by the user for all three train, dev and test
usr1 = User.query.filter_by(email='disooqi@gmail.com').first()
n_link_requested = len(usr1.mgb2_downloads)


# Number of download trials  for a specific user
usr1_total = 0
for lnk in usr1.mgb2_downloads:
	usr1_total += lnk.n_downloads
else:
    print(usr1_total)


