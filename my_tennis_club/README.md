# Django Guide for Rails Developers

A comprehensive guide to understanding Django's structure, concepts, and workflows coming from a Ruby on Rails background.

## Table of Contents
- [Quick Comparison: Django vs Rails](#quick-comparison-django-vs-rails)
- [Core Concepts](#core-concepts)
- [Project Structure](#project-structure)
- [How Django Loads Files](#how-django-loads-files)
- [Registration & Configuration](#registration--configuration)
- [MVC vs MVT Pattern](#mvc-vs-mvt-pattern)
- [Common Tasks Comparison](#common-tasks-comparison)
- [Key Differences to Remember](#key-differences-to-remember)

---

## Quick Comparison: Django vs Rails

| Aspect | Rails | Django |
|--------|-------|--------|
| **Language** | Ruby | Python |
| **Pattern** | MVC (Model-View-Controller) | MVT (Model-View-Template) |
| **Philosophy** | Convention over Configuration | Explicit is better than implicit |
| **Routing** | `config/routes.rb` (centralized) | URLconfs - `urls.py` (can be modular) |
| **Views** | ERB/Haml templates | Django Templates (or Jinja2) |
| **Controllers** | `app/controllers/` | Views (`views.py`) |
| **Models** | ActiveRecord | Django ORM |
| **Migrations** | `db/migrate/` | `migrations/` folder per app |
| **Asset Pipeline** | Sprockets/Webpacker | Static files system |
| **Admin Interface** | Needs gems (ActiveAdmin) | Built-in (`/admin`) |
| **Test Framework** | Minitest/RSpec | unittest/pytest |
| **Package Manager** | Bundler (Gemfile) | pip (requirements.txt) |
| **Server** | Puma/Unicorn | WSGI (Gunicorn/uWSGI) |

---

## Core Concepts

### 1. **Projects vs Apps**

**Rails equivalent**: In Rails, you have ONE application.

**Django**: You have a **project** containing multiple **apps**.

- **Project** = The entire website (like `my_tennis_club/`)
  - Contains settings, main URL configuration, WSGI/ASGI config
  
- **App** = A modular component (like `members/`)
  - Reusable, pluggable modules
  - Each app has its own models, views, templates, URLs
  - Similar to Rails engines, but more common

```
Rails:    blog/              (one app)
Django:   my_site/           (project)
            ├── blog/        (app)
            ├── users/       (app)
            └── comments/    (app)
```

### 2. **MVT Pattern (Model-View-Template)**

| Rails MVC | Django MVT | Purpose |
|-----------|------------|---------|
| **Model** | **Model** | Database layer (same concept) |
| **Controller** | **View** | Business logic (confusing, I know!) |
| **View** | **Template** | Presentation layer |

**Important**: Django's "Views" are like Rails "Controllers"!

### 3. **Explicit Configuration**

Rails uses lots of magic and conventions. Django requires you to be explicit:

- Apps must be registered in `INSTALLED_APPS`
- URLs must be explicitly defined
- Database relationships must be explicitly declared
- Middleware must be listed in order

---

## Project Structure

```
my_tennis_club/                    # Project root directory
│
├── manage.py                      # Rails: like 'rails' command
│                                  # Used for: runserver, migrate, shell, etc.
│
├── db.sqlite3                     # Database file (like Rails db/development.sqlite3)
│
├── my_tennis_club/                # Project configuration directory
│   │                              # Rails equivalent: config/
│   │
│   ├── __init__.py                # Makes this a Python package
│   ├── settings.py                # Rails: config/application.rb + config/environments/
│   ├── urls.py                    # Rails: config/routes.rb (root URL config)
│   ├── wsgi.py                    # WSGI config (like config.ru)
│   └── asgi.py                    # ASGI config (for async/WebSockets)
│
└── members/                       # App directory (like one section of your Rails app)
    │                              # Rails equivalent: app/models/member.rb, app/controllers/members_controller.rb
    │
    ├── __init__.py                # Makes this a Python package
    ├── admin.py                   # Register models for Django admin
    ├── apps.py                    # App configuration
    ├── models.py                  # Rails: app/models/
    ├── views.py                   # Rails: app/controllers/
    ├── urls.py                    # URL patterns for this app (optional)
    ├── tests.py                   # Rails: test/ or spec/
    │
    ├── migrations/                # Rails: db/migrate/
    │   ├── __init__.py
    │   └── 0001_initial.py
    │
    └── templates/                 # Rails: app/views/
        └── myfirst.html
```

### File Purposes

#### **manage.py** (Project Root)
```bash
# Rails equivalent commands:
python manage.py runserver      # rails server
python manage.py migrate        # rails db:migrate
python manage.py makemigrations # rails generate migration
python manage.py shell          # rails console
python manage.py createsuperuser # rails console -> User.create(admin: true)
python manage.py test           # rails test
```

#### **settings.py** (Project Configuration)
This is like Rails' `config/application.rb`, `config/database.yml`, and `config/environments/*.rb` combined.

```python
# Key settings:
DEBUG = True                    # Rails: development mode
ALLOWED_HOSTS = []              # Security: which domains can serve this app
INSTALLED_APPS = [...]          # Apps to load (MUST register your apps here!)
MIDDLEWARE = [...]              # Rails: config.middleware
DATABASES = {...}               # Rails: config/database.yml
STATIC_URL = '/static/'         # Rails: asset pipeline
TEMPLATES = [...]               # Template engine config
```

#### **urls.py** (URL Configuration)
Rails: `config/routes.rb`
Django: `urls.py`

```python
# Project-level urls.py (my_tennis_club/urls.py)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members.urls')),  # Include app URLs
]
```

```python
# App-level urls.py (members/urls.py)
from django.urls import path
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    # Rails equivalent: get 'members', to: 'members#index', as: 'members'
]
```

#### **models.py** (Database Models)
Rails: `app/models/*.rb`
Django: `models.py`

```python
from django.db import models

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    
    # Rails: belongs_to :team
    # Django:
    team = models.ForeignKey('Team', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    class Meta:
        db_table = 'members'
        ordering = ['lastname']
```

#### **views.py** (Request Handlers)
Rails: `app/controllers/*_controller.rb`
Django: `views.py`

```python
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Member

# Function-based view (simple)
def members(request):
    members = Member.objects.all()
    context = {'members': members}
    return render(request, 'members.html', context)
    # Rails: @members = Member.all; render :members

# Class-based view (like Rails controllers)
from django.views.generic import ListView

class MemberListView(ListView):
    model = Member
    template_name = 'members.html'
    context_object_name = 'members'
```

#### **admin.py** (Admin Interface)
**No Rails equivalent** - this is unique to Django!
Django has a built-in admin interface that you can customize here.

```python
from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname']
    search_fields = ['firstname', 'lastname']
```

---

## How Django Loads Files

### 1. **Server Startup**
```
1. manage.py runserver
2. Loads my_tennis_club/settings.py
3. Reads INSTALLED_APPS
4. Imports each app's models, admin, etc.
5. Loads ROOT_URLCONF (urls.py)
6. Applies MIDDLEWARE
7. Server ready!
```

### 2. **Request Cycle**
```
1. Request arrives: GET /members/
2. Django loads ROOT_URLCONF (my_tennis_club/urls.py)
3. Matches URL pattern → routes to app URLs
4. App urls.py matches pattern → calls view function
5. View function executes (queries database, etc.)
6. View renders template with context
7. Returns HttpResponse
```

**Rails equivalent**:
```
Request → routes.rb → MembersController#index → render view
Django:
Request → urls.py → members/urls.py → views.members() → render template
```

### 3. **Import System**

Django uses Python's import system. Key rules:

```python
# Absolute imports (preferred)
from members.models import Member
from django.shortcuts import render

# Relative imports (within same app)
from .models import Member  # Same directory
from ..utils import helper  # Parent directory
```

---

## Registration & Configuration

### **Apps Must Be Registered!**

Unlike Rails (which auto-loads `app/models`), Django requires explicit registration.

#### Step 1: Create app
```bash
python manage.py startapp members
```

#### Step 2: Register in settings.py
```python
# my_tennis_club/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'members',  # ← ADD YOUR APP HERE!
]
```

### **Models Must Be Registered for Admin**

```python
# members/admin.py
from django.contrib import admin
from .models import Member

admin.site.register(Member)
```

### **URLs Must Be Connected**

```python
# Project urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('members.urls')),  # Connect app URLs
]
```

### **Migrations Must Be Created & Applied**

```bash
# After creating/changing models:
python manage.py makemigrations  # Create migration files
python manage.py migrate         # Apply to database
```

Rails: `rails generate model` creates migration automatically.
Django: You create model first, then generate migration separately.

---

## MVC vs MVT Pattern

### Rails MVC Flow:
```
Request → routes.rb → MembersController → @members = Member.all → members.html.erb
```

### Django MVT Flow:
```
Request → urls.py → views.members() → members = Member.objects.all() → members.html
```

### Side-by-Side Example

**Rails**: Creating a members list

```ruby
# config/routes.rb
get 'members', to: 'members#index'

# app/controllers/members_controller.rb
class MembersController < ApplicationController
  def index
    @members = Member.all
  end
end

# app/views/members/index.html.erb
<% @members.each do |member| %>
  <%= member.name %>
<% end %>

# app/models/member.rb
class Member < ApplicationRecord
end
```

**Django**: Same feature

```python
# members/urls.py
path('members/', views.members, name='members')

# members/views.py
def members(request):
    members = Member.objects.all()
    return render(request, 'members.html', {'members': members})

# templates/members.html
{% for member in members %}
  {{ member.name }}
{% endfor %}

# members/models.py
class Member(models.Model):
    name = models.CharField(max_length=255)
```

---

## Common Tasks Comparison

### Creating a New Model

**Rails**:
```bash
rails generate model Member firstname:string lastname:string
rails db:migrate
```

**Django**:
```bash
# 1. Edit members/models.py
# 2. Add model class
# 3. Generate migration
python manage.py makemigrations
python manage.py migrate
```

### Database Queries

| Rails | Django |
|-------|--------|
| `Member.all` | `Member.objects.all()` |
| `Member.find(1)` | `Member.objects.get(id=1)` |
| `Member.where(firstname: 'John')` | `Member.objects.filter(firstname='John')` |
| `Member.create(name: 'John')` | `Member.objects.create(name='John')` |
| `member.update(name: 'Jane')` | `member.name = 'Jane'; member.save()` |
| `member.destroy` | `member.delete()` |
| `Member.joins(:team)` | `Member.objects.select_related('team')` |
| `Member.includes(:posts)` | `Member.objects.prefetch_related('posts')` |

### Forms

**Rails**: 
```ruby
<%= form_for @member do |f| %>
  <%= f.text_field :name %>
<% end %>
```

**Django**:
```python
# forms.py
from django import forms

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['firstname', 'lastname']

# template
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Submit</button>
</form>
```

### Validations

**Rails**:
```ruby
class Member < ApplicationRecord
  validates :firstname, presence: true
  validates :email, uniqueness: true
end
```

**Django**:
```python
class Member(models.Model):
    firstname = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True)
    
    def clean(self):
        # Custom validation
        if not self.firstname:
            raise ValidationError('First name is required')
```

### Associations

**Rails**:
```ruby
class Member < ApplicationRecord
  belongs_to :team
  has_many :posts
end

class Team < ApplicationRecord
  has_many :members
end
```

**Django**:
```python
class Team(models.Model):
    name = models.CharField(max_length=255)

class Member(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    # Access: member.team
    # Reverse: team.members.all()

class Post(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='posts')
```

---

## Key Differences to Remember

### 1. **No Magic**
- Rails: Auto-loads files from `app/`
- Django: Must explicitly register apps, import modules

### 2. **App Structure**
- Rails: One app with organized folders
- Django: Multiple apps, each self-contained

### 3. **Templates**
- Rails: ERB `<%= %>` and `<% %>`
- Django: `{{ }}` and `{% %}`

### 4. **URL Routing**
- Rails: Centralized `routes.rb`
- Django: Can be split across apps (modular)

### 5. **Migrations**
- Rails: Generated when you generate model
- Django: Manually run `makemigrations` after model changes

### 6. **Console/Shell**
- Rails: `rails console`
- Django: `python manage.py shell`

### 7. **Built-in Admin**
- Rails: Need gems (ActiveAdmin)
- Django: Built-in, just register models

### 8. **ORM Methods**
- Rails: Direct methods `Member.all`
- Django: Manager `Member.objects.all()`

### 9. **Settings**
- Rails: Multiple files in `config/`
- Django: One `settings.py` (can split later)

### 10. **Python vs Ruby**
- Indentation matters in Python!
- `__init__.py` makes directories into packages
- Use `self` instead of implicit `@`

---

## Essential Commands

```bash
# Create project
django-admin startproject my_tennis_club

# Create app
python manage.py startapp members

# Run development server
python manage.py runserver

# Database
python manage.py makemigrations  # Create migrations
python manage.py migrate         # Apply migrations
python manage.py showmigrations  # List migrations

# Admin
python manage.py createsuperuser

# Shell
python manage.py shell

# Testing
python manage.py test

# Static files
python manage.py collectstatic
```

---

## Quick Start Workflow

1. **Create project**: `django-admin startproject myproject`
2. **Create app**: `python manage.py startapp myapp`
3. **Register app** in `settings.py` → `INSTALLED_APPS`
4. **Create models** in `myapp/models.py`
5. **Make migrations**: `python manage.py makemigrations`
6. **Migrate**: `python manage.py migrate`
7. **Register models** in `myapp/admin.py` (for admin interface)
8. **Create views** in `myapp/views.py`
9. **Create templates** in `myapp/templates/`
10. **Configure URLs** in `myapp/urls.py` and include in project `urls.py`
11. **Run server**: `python manage.py runserver`

---

## Helpful Tips

- **Settings**: Use environment variables for secrets (like Rails credentials)
- **Apps**: Keep apps focused and reusable
- **Templates**: Use template inheritance (`{% extends %}`)
- **Static files**: Put in `static/` folder in each app
- **Testing**: Django's test client is similar to Rails system tests
- **Debugging**: Install `django-debug-toolbar` (like Rails web-console)
- **REST API**: Use `djangorestframework` (like Rails API mode)

---

## Resources

- [Official Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [Django for Rails Developers](https://www.djangoproject.com/)
- [Django ORM Cookbook](https://books.agiliq.com/projects/django-orm-cookbook/en/latest/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x) (Best practices book)

---

## Your Current Project Structure

```
my_tennis_club/           # Project root
├── manage.py            # CLI tool
├── db.sqlite3           # Database
├── my_tennis_club/      # Project settings
│   ├── settings.py      # Main configuration
│   └── urls.py          # Root URL config
└── members/             # Your first app
    ├── models.py        # Define Member model here
    ├── views.py         # Request handlers
    ├── urls.py          # App-specific URLs
    ├── admin.py         # Register for admin
    └── templates/       # HTML templates
```

**Next steps for your project**:
1. Define a `Member` model in `members/models.py`
2. Run `python manage.py makemigrations` and `python manage.py migrate`
3. Register the model in `members/admin.py`
4. Create a superuser: `python manage.py createsuperuser`
5. Visit `http://localhost:8000/admin/` to see the Django admin!

Happy Django-ing! 🎾🐍

