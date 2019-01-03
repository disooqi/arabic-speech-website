pip install alembic
alembic init alembic
###
# edit alembic.ini
# sqlalchemy.url = sqlite:///arabic_speech_community/arabic_speech.db
###
alembic revision -m "Add a column"

  263  alembic upgrade head
  264  python
  265  scp speech@arabicspeech.org:/work/arabic-speech-website/arabic_speech_community/arabic_speech.db OK
  266  python readDB.py
  267  ls -lt
  268  ls arabic_speech_community/
  269  cp  arabic_speech_community/arabic_speech.db arabic_speech_community/arabic_speech.db.ok
  270  python modifyDB.py
  271  python readDB.py
  272  python readDB.py  | grep amali
  273  python modifyDB.py
  274  ls -ltr
  275  cat OK
  276  rm OK
  277  ls -ltr
  278  scp speech@arabicspeech.org:/work/arabic-speech-website/arabic_speech_community/arabic_speech.db OK
  279  scp speech@arabicspeech.org:/work/arabic-speech-website/arabic_speech_community/arabic_speech.db arabic_speech_community/arabic_speech.db
  280  history