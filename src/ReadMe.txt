p
Step 1:
First create virtual environment with this command:

- virtualenv ConsumerProtection

A new folder will be created called ConsumerProtection

Step 2:
Open ConsumerProtection folder
Paste or extract src into ConsumerProtection folder

Step 3:
Create database called consumer_protection under user postgres and make changes to your settings.py file with the new database configuration.

Note: If your database configs are incorrect, your app will not run

Step 4:
Open ConsumerProtection in Pycharm and type these commands:
- pip install -r requirements.txt
- python manage.py makemigrations
- python manage.py migrate
- python manage.py runserver

DONE!!!