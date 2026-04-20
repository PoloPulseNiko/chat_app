# NTChat

NTChat is a Django community chat platform built for the Django Advanced course project. It combines public informational pages, profile-driven social features, topic-based rooms, message reactions, in-app notifications, a staff-only management panel, REST API endpoints, and asynchronous background notification processing.

## Project Idea

The application is designed as a room-based discussion platform where users can:

- register and log in with a custom user model
- receive an automatically created profile
- upload a profile picture
- browse profiles and public informational pages
- create and manage discussion rooms
- join rooms and participate in message threads
- react to messages
- receive private notifications when room activity happens
- access a personal dashboard
- access a separate staff dashboard for moderation and monitoring

## Main Features

- Custom `ChatUser` model extending Django `AbstractUser`
- One-to-one user profile with nickname, bio, and avatar
- Automatic profile creation after signup
- Public homepage, About, FAQ, and Community Guidelines pages
- Public profile list and profile details
- Room categories, tags, and memberships
- Owner-managed CRUD for profiles, rooms, and messages
- Message reactions (`Like`, `Love`, `Laugh`)
- Notification center with filters and mark-as-read actions
- Private user dashboard
- Separate in-app staff panel
- REST API endpoints with serializers and permissions
- Async notification creation using background threads and `asyncio`
- Custom template filters for reactions and unread notifications
- Custom 404 and 500 pages

## Application Structure

The project contains 6 Django apps:

- `accounts_app`  
  Custom user model, signup flow, group creation, and profile helper logic.

- `profiles_app`  
  Public profiles, profile editing, profile deletion, avatar support, and private dashboard.

- `rooms_app`  
  Categories, tags, rooms, memberships, room CRUD, room filtering, and room API endpoints.

- `messages_app`  
  Room messages, message editing/deletion, and message reactions.

- `notifications_app`  
  Private notifications, filtering, API endpoint, and async notification dispatch.

- `staff_panel_app`  
  Staff-only dashboard with statistics and broadcast notifications.

## Database Models

The project currently includes these models:

- `ChatUser`
- `Profile`
- `Category`
- `Tag`
- `Room`
- `Membership`
- `Message`
- `Reaction`
- `Notification`

## Relationships

Examples of many-to-one relationships:

- `Profile -> ChatUser`
- `Room -> Profile` as creator
- `Room -> Category`
- `Message -> Profile`
- `Message -> Room`
- `Notification -> Profile`
- `Notification -> Room`

Examples of many-to-many relationships:

- `Room.members -> Profile`
- `Room.tags -> Tag`

## Authentication, Roles, and Permissions

- User registration, login, and logout are implemented.
- The built-in Django user system is extended through `ChatUser`.
- Each new user automatically gets a `Profile`.
- Two groups are created automatically after migration:
  - `Moderators`
  - `Room Managers`
- A dedicated in-app `Staff Panel` exists separately from the built-in Django admin.

## Forms and Validation

The project includes these forms:

- `SignUpForm`
- `ProfileForm`
- `RoomForm`
- `RoomFilterForm`
- `MessageForm`
- `NotificationFilterForm`
- `BroadcastNotificationForm`

Validation and UX details include:

- custom validation messages
- labels, help texts, and placeholders
- read-only fields in profile and room forms
- confirmation pages for delete actions
- avatar upload support through the profile form

## Views and API

The app uses class-based views as the main approach across profiles, rooms, messages, notifications, staff pages, and signup.

REST API functionality includes:

- `GET /rooms/api/`
- `GET /rooms/api/<id>/`
- `GET /rooms/api/<id>/messages/`
- `GET /notifications/api/`

## Asynchronous Processing

The project includes asynchronous notification dispatch in `notifications_app/tasks.py`.

Current async behavior:

- notify room members about new messages
- notify members about room updates
- send staff broadcast notifications to room members

## Templates and Pages

The project includes more than 15 templates/pages, including:

- homepage
- about page
- FAQ page
- community guidelines page
- login page
- signup page
- profile list
- profile details
- profile form
- profile delete confirmation
- user dashboard
- room list
- room details
- room form
- room delete confirmation
- message delete confirmation
- message form
- notifications page
- staff dashboard
- custom 404 page
- custom 500 page

Reusable layout support includes:

- shared base template
- shared navbar
- shared footer
- custom template tags

## Media Handling

The project supports user profile pictures through `ImageField`.

- uploaded avatars are stored in `profile_pictures/`
- profile pictures are displayed on profile pages
- avatars are displayed in room conversations and room header metadata
- media configuration is included in project settings and URL routing

## Automated Tests

The repository contains 23 automated tests covering:

- signup and automatic profile creation
- default groups
- public/private page access
- owner-only edit restrictions
- room creation and membership behavior
- message reactions
- notifications and filtering
- API behavior
- staff access rules

Test command:

```bash
python manage.py test --settings=chat_project.test_settings
```

## Tech Stack

- Python 3.13
- Django 6.0.2
- Django REST Framework 3.17.1
- PostgreSQL
- Bootstrap 5
- Pillow
- WhiteNoise

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repository-url>
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

The project uses environment variables for deployment-sensitive configuration.

For local development without Azure, the project can still run with SQLite defaults if no Azure PostgreSQL connection string is provided.

Example local `.env` values:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
```

For Azure deployment, configure:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-app.azurewebsites.net
DJANGO_CSRF_TRUSTED_ORIGINS=https://your-app.azurewebsites.net
AZURE_POSTGRESQL_CONNECTIONSTRING=your-azure-postgresql-connection-string
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 7. Run the server

```bash
python manage.py runserver
```

## Deployment Notes

- The deployed version is configured for Azure App Service on Linux.
- PostgreSQL is used in production through Azure environment variables.
- Static files are served with WhiteNoise.
- Media files are configured through Django media settings.
- A separate startup script is included for cloud deployment.

## Requirement Coverage Summary

This project covers the core exam requirements through:

- 6 Django apps
- 9 database models
- extended user model
- public and private sections
- authentication system
- user groups and permissions
- 7 forms
- owner-managed CRUD
- CBV-heavy architecture
- DRF API endpoints
- async background processing
- media upload handling
- custom error pages
- reusable templates and navigation
- 23 automated tests

## Admin and Staff Features

- Built-in Django admin is available at `/admin/`
- Separate in-app staff dashboard is available at `/staff-panel/`
- Staff users can review platform statistics and send room broadcasts

## Custom Template Utilities

Custom template filters in `rooms_app/templatetags/chat_tags.py`:

- `reaction_count`
- `unread_notifications_count`

## Author

Project created by Niko for the Django Advanced course project.
