# Palendar - Calendar for Teamspaces
SPbETU "LETI" Educational practice.

----
## How to setup
1. Make migrations for Databases: `python manage.py makemigrations`
2. Migrate: `python manage.py migrate`
3. Prepare Superuser if needed: `python manage.py createsuperuser`
4. Run server on localhost: `python manage.py runserver`

____
## Modules

### User
Responsible for the Users in the system.
Provides registration/login/password change capabilities, 
also a calendar invitation system

### Event
Responsible for the Events in the system.
Provides the ability to create/edit/view events,
displaying them in the form of a calendar, etc.

### Chat
Responsible for the Chat in the system.
Provides events with messaging functionality between participants
