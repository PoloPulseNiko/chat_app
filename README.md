# Chat Project

Chat Project is a community chat platform built with Django and Django REST Framework. Users can register, manage profiles, create topic-based rooms, join conversations, react to messages, receive notifications, and access private dashboards. Staff users also get a separate in-app staff panel for moderation and overview tasks outside the built-in Django admin.

## Features

- Public room and profile browsing
- Custom user model with registration, login, and logout
- Automatic profile creation for new users
- Private user dashboard with recent rooms, messages, and notifications
- Staff-only dashboard with platform statistics and room broadcast notifications
- Room categories, tags, memberships, and owner-managed room CRUD
- Message posting, editing, deleting, and reactions
- In-app notifications with filtering and mark-as-read actions
- REST API endpoints for rooms, room messages, and authenticated notifications
- Async notification dispatch using asyncio-based background tasks

## Apps

- `accounts_app` - custom user model, signup flow, groups, and authentication helpers
- `profiles_app` - public profiles and private user dashboard
- `rooms_app` - rooms, categories, tags, memberships, filters, and room API
- `messages_app` - room messages, reactions, and owner-only message management
- `notifications_app` - in-app notifications, filters, API, and async dispatch
- `staff_panel_app` - staff-only dashboard and broadcast tools

## Models

- `ChatUser`
- `Profile`
- `Category`
- `Tag`
- `Room`
- `Membership`
- `Message`
- `Reaction`
- `Notification`

## Tech Stack

- Python 3.13
- Django 6.0.2
- Django REST Framework 3.17.1
- PostgreSQL
- Bootstrap 5

## Requirements Coverage

- Public and private sections
- Extended user model
- 6 Django apps
- 9 database models
- Multiple many-to-one and many-to-many relationships
- Owner-managed CRUD for profiles, rooms, and messages
- CBV-heavy implementation
- DRF API endpoints
- Async notification processing
- 23 automated tests

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd chat_project
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` and set the values for your machine. The project reads its configuration from environment variables and also provides safe local defaults.

Example environment values:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DB_NAME=chat_app
DB_USER=postgres-user
DB_PASSWORD=password
DB_HOST=127.0.0.1
DB_PORT=5432
```

You can export them manually before running the server:

```bash
export DJANGO_SECRET_KEY="change-me"
export DJANGO_DEBUG="True"
export DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
export DB_NAME="chat_app"
export DB_USER="postgres-user"
export DB_PASSWORD="password"
export DB_HOST="127.0.0.1"
export DB_PORT="5432"
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Main URLs

- `/rooms/` - public room list
- `/profiles/` - public profile list
- `/accounts/signup/` - registration
- `/accounts/login/` - login
- `/profiles/dashboard/` - private user dashboard
- `/notifications/` - private notifications page
- `/staff-panel/` - staff-only in-app dashboard
- `/admin/` - Django admin

## API Endpoints

- `/rooms/api/` - list all rooms
- `/rooms/api/<id>/` - room details
- `/rooms/api/<id>/messages/` - messages for a room
- `/notifications/api/` - authenticated user notifications

## Async Processing

The project includes asyncio-based background notification dispatch:

- new room messages notify other room members
- room updates notify existing members
- staff broadcasts notify members of a selected room

The async logic lives in [notifications_app/tasks.py](./notifications_app/tasks.py).

## Testing

The project includes 23 automated tests. They can be run with the dedicated SQLite test settings:

```bash
python manage.py test --settings=chat_project.test_settings
```

## Deployment Notes

- Use PostgreSQL in production
- Set environment variables through your cloud provider configuration
- Run `python manage.py collectstatic` before deployment
- Set `DJANGO_DEBUG=False` in production
- Add the deployed domain to `DJANGO_ALLOWED_HOSTS`

## Default Groups

The following groups are created automatically after migrations:

- `Moderators`
- `Room Managers`

## Custom Template Utilities

The project includes custom template helpers in `rooms_app/templatetags/chat_tags.py`:

- `reaction_count`
- `unread_notifications_count`
