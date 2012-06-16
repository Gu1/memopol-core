How to translate Memopol2 ?
===========================

- Go to the source folder (the same folder where this README file is located)

- Check that you don't already have your translation in locale/<your language code>

If not :

- Create locale directory if needed :
  mkdir locale

- Create messages for your language (ex for french)
  django-admin.py makemessages -l fr

- if you have conflicts with your virtualenv use the "--ignore" option of
  makemessages like this (supposing your virtualenv is named "ve"):
  django-admin.py makemessages -l fr --ignore="ve/*"

- Go to the po file directory :
  cd locale/fr/LC_MESSAGES

- Edit the po file :
  vi django.po

- Translate the "msgid" (don't touch them) in the "msgstr" strings

- Send us the .po file either through git or by mail.

- You can also compile your translations to test them:
  django-admin.py compilemessages
