# Chat Project

A simple Django-based chat application featuring user profiles, rooms, and messages. Users can create and edit profiles, create rooms, send messages, and manage content.

## Features

- **Profiles**: Create, edit, and view user profiles.  
- **Rooms**: Create, edit, delete, and browse chat rooms.  
- **Messages**: Send, edit, and delete messages in rooms.  
- **PostgreSQL** database backend using `psycopg[binary]`.  

## Installation

### Prerequisites

- Python 3.13  
- Django 6.0+  
- PostgreSQL  

### Setup

1. Clone the repository:

git clone <your-repo-url>
cd chat_project
Create and activate a virtual environment:
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
Install dependencies:
pip install Django==6.0.2 "psycopg[binary]"
Configure your database in chat_project/settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chat_app',
        'USER': 'postgres-user',
        'PASSWORD': '<your-db-password>',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
Apply database migrations:
python manage.py migrate
Create a superuser (optional):
python manage.py createsuperuser
Start the development server:
python manage.py runserver
Open your browser at:
http://127.0.0.1:8000/
Project Structure
chat_project/
│
├── chat_project/          # Django project settings
├── profiles_app/          # User profiles
├── rooms_app/             # Chat rooms
├── messages_app/          # Chat messages
└── manage.py
URLs / Navigation
Profiles
/profiles/ - list
/profiles/<int:pk>/ - detail
/profiles/create/, /profiles/<int:pk>/edit/, /profiles/<int:pk>/delete/
Rooms
/rooms/ - list
/rooms/<int:pk>/ - detail
/rooms/create/, /rooms/<int:pk>/edit/, /rooms/<int:pk>/delete/
Messages
/messages/<int:pk>/edit/ - edit
/messages/<int:pk>/delete/ - delete
