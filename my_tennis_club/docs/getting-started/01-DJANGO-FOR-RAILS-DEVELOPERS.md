# Django Guide for Rails Developers

A comprehensive guide to understanding Django's structure, concepts, and workflows coming from a Ruby on Rails background.

## Table of Contents
- [Quick Comparison: Django vs Rails](#quick-comparison-django-vs-rails)
- [Core Concepts](#core-concepts)
- [Project Structure](#project-structure)
- [How Django Loads Files](#how-django-loads-files)
- [Registration & Configuration](#registration--configuration)
- [MVC vs MVT Pattern](#mvc-vs-mvt-pattern)
- [CRUD Operations: NEW, EDIT, INDEX, UPDATE, DELETE, CREATE](#crud-operations-new-edit-index-update-delete-create)
- [AJAX Requests in Django](#ajax-requests-in-django)
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

## CRUD Operations: NEW, EDIT, INDEX, UPDATE, DELETE, CREATE

Django doesn't have Rails' convention-based actions (`index`, `new`, `create`, etc.). Instead, you explicitly define views and URL patterns. Here's how to handle each operation:

### Quick Comparison

| Rails Action | HTTP Method | Django Equivalent | Purpose |
|--------------|-------------|-------------------|---------|
| `index` | GET | List view | Display all records |
| `show` | GET | Detail view | Display one record |
| `new` | GET | Form view | Show creation form |
| `create` | POST | Form view (POST) | Process creation |
| `edit` | GET | Form view | Show edit form |
| `update` | PATCH/PUT | Form view (POST) | Process update |
| `destroy` | DELETE | Delete view | Delete record |

### Method 1: Function-Based Views (FBV)

This is the most explicit way, similar to writing individual controller actions in Rails.

#### Complete CRUD Example

```python
# members/models.py
from django.db import models

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    joined_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    class Meta:
        ordering = ['lastname', 'firstname']
```

```python
# members/forms.py
from django import forms
from .models import Member

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['firstname', 'lastname', 'email', 'phone']
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
```

```python
# members/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Member
from .forms import MemberForm

# INDEX - List all members (Rails: index action)
def member_list(request):
    members = Member.objects.all()
    context = {'members': members}
    return render(request, 'members/index.html', context)

# SHOW - Display single member (Rails: show action)
def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    context = {'member': member}
    return render(request, 'members/show.html', context)

# NEW + CREATE - Show form and handle submission (Rails: new + create actions)
def member_create(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            messages.success(request, f'Member {member} created successfully!')
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm()
    
    context = {'form': form, 'action': 'Create'}
    return render(request, 'members/form.html', context)

# EDIT + UPDATE - Show form and handle submission (Rails: edit + update actions)
def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, f'Member {member} updated successfully!')
            return redirect('member_detail', pk=member.pk)
    else:
        form = MemberForm(instance=member)
    
    context = {'form': form, 'member': member, 'action': 'Update'}
    return render(request, 'members/form.html', context)

# DELETE - Delete member (Rails: destroy action)
def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    
    if request.method == 'POST':
        member_name = str(member)
        member.delete()
        messages.success(request, f'Member {member_name} deleted successfully!')
        return redirect('member_list')
    
    context = {'member': member}
    return render(request, 'members/confirm_delete.html', context)
```

```python
# members/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # INDEX
    path('', views.member_list, name='member_list'),
    
    # SHOW
    path('<int:pk>/', views.member_detail, name='member_detail'),
    
    # NEW/CREATE
    path('new/', views.member_create, name='member_create'),
    
    # EDIT/UPDATE
    path('<int:pk>/edit/', views.member_update, name='member_update'),
    
    # DELETE
    path('<int:pk>/delete/', views.member_delete, name='member_delete'),
]

# Rails equivalent:
# resources :members
```

```python
# my_tennis_club/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('members/', include('members.urls')),
]
```

#### Templates

```html
<!-- templates/members/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Members</title>
</head>
<body>
    <h1>Members</h1>
    <a href="{% url 'member_create' %}">New Member</a>
    
    {% if messages %}
        {% for message in messages %}
            <div class="alert">{{ message }}</div>
        {% endfor %}
    {% endif %}
    
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for member in members %}
            <tr>
                <td>{{ member.firstname }} {{ member.lastname }}</td>
                <td>{{ member.email }}</td>
                <td>
                    <a href="{% url 'member_detail' member.pk %}">Show</a>
                    <a href="{% url 'member_update' member.pk %}">Edit</a>
                    <a href="{% url 'member_delete' member.pk %}">Delete</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="3">No members yet.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```

```html
<!-- templates/members/show.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ member }}</title>
</head>
<body>
    <h1>{{ member.firstname }} {{ member.lastname }}</h1>
    
    <p><strong>Email:</strong> {{ member.email }}</p>
    <p><strong>Phone:</strong> {{ member.phone|default:"N/A" }}</p>
    <p><strong>Joined:</strong> {{ member.joined_date|date:"F d, Y" }}</p>
    
    <a href="{% url 'member_list' %}">Back to List</a>
    <a href="{% url 'member_update' member.pk %}">Edit</a>
    <a href="{% url 'member_delete' member.pk %}">Delete</a>
</body>
</html>
```

```html
<!-- templates/members/form.html -->
<!DOCTYPE html>
<html>
<head>
    <title>{{ action }} Member</title>
</head>
<body>
    <h1>{{ action }} Member</h1>
    
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">{{ action }}</button>
        <a href="{% url 'member_list' %}">Cancel</a>
    </form>
    
    {% if form.errors %}
        <div class="errors">
            {{ form.errors }}
        </div>
    {% endif %}
</body>
</html>
```

```html
<!-- templates/members/confirm_delete.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Delete Member</title>
</head>
<body>
    <h1>Delete Member</h1>
    
    <p>Are you sure you want to delete <strong>{{ member }}</strong>?</p>
    
    <form method="post">
        {% csrf_token %}
        <button type="submit">Yes, Delete</button>
        <a href="{% url 'member_detail' member.pk %}">Cancel</a>
    </form>
</body>
</html>
```

### Method 2: Class-Based Views (CBV)

Django provides generic class-based views that are similar to Rails scaffolding but more powerful.

```python
# members/views.py
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Member
from .forms import MemberForm

# INDEX
class MemberListView(ListView):
    model = Member
    template_name = 'members/index.html'
    context_object_name = 'members'
    # Rails: def index; @members = Member.all; end

# SHOW
class MemberDetailView(DetailView):
    model = Member
    template_name = 'members/show.html'
    context_object_name = 'member'
    # Rails: def show; @member = Member.find(params[:id]); end

# NEW/CREATE
class MemberCreateView(SuccessMessageMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'members/form.html'
    success_url = reverse_lazy('member_list')
    success_message = "Member %(firstname)s %(lastname)s created successfully!"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Create'
        return context
    # Rails: def new; @member = Member.new; end
    #        def create; @member = Member.new(params); @member.save; end

# EDIT/UPDATE
class MemberUpdateView(SuccessMessageMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'members/form.html'
    success_message = "Member %(firstname)s %(lastname)s updated successfully!"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context
    
    def get_success_url(self):
        return reverse_lazy('member_detail', kwargs={'pk': self.object.pk})
    # Rails: def edit; @member = Member.find(params[:id]); end
    #        def update; @member.update(params); end

# DELETE
class MemberDeleteView(SuccessMessageMixin, DeleteView):
    model = Member
    template_name = 'members/confirm_delete.html'
    success_url = reverse_lazy('member_list')
    success_message = "Member deleted successfully!"
    # Rails: def destroy; @member.destroy; end
```

```python
# members/urls.py (for Class-Based Views)
from django.urls import path
from . import views

urlpatterns = [
    path('', views.MemberListView.as_view(), name='member_list'),
    path('<int:pk>/', views.MemberDetailView.as_view(), name='member_detail'),
    path('new/', views.MemberCreateView.as_view(), name='member_create'),
    path('<int:pk>/edit/', views.MemberUpdateView.as_view(), name='member_update'),
    path('<int:pk>/delete/', views.MemberDeleteView.as_view(), name='member_delete'),
]
```

### Key Differences from Rails

| Aspect | Rails | Django |
|--------|-------|--------|
| **Routing** | `resources :members` auto-creates 7 routes | Must define each URL explicitly |
| **Actions** | Separate methods: `new` & `create` | Single view handles both GET & POST |
| **HTTP Methods** | Uses PUT/PATCH/DELETE | Typically uses GET & POST (can use others) |
| **Forms** | `form_for @member` | `ModelForm` class + `{{ form }}` |
| **CSRF** | Auto-included | Must add `{% csrf_token %}` |
| **Redirects** | `redirect_to @member` | `redirect('member_detail', pk=member.pk)` |
| **Flash Messages** | `flash[:notice]` | `messages.success(request, ...)` |
| **Strong Params** | `params.require(:member).permit(...)` | Form validation handles this |

---

## AJAX Requests in Django

Django handles AJAX differently than Rails. There's no built-in `respond_to` block, but it's straightforward to detect AJAX requests and return JSON.

### Method 1: Detecting AJAX Requests

```python
# members/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["GET", "POST"])
def member_api(request):
    # Check if it's an AJAX request
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    if request.method == 'POST':
        if is_ajax:
            # Handle AJAX POST
            data = json.loads(request.body)
            member = Member.objects.create(
                firstname=data.get('firstname'),
                lastname=data.get('lastname'),
                email=data.get('email')
            )
            return JsonResponse({
                'success': True,
                'member': {
                    'id': member.pk,
                    'name': str(member),
                    'email': member.email
                }
            })
        else:
            # Handle regular POST
            # ... normal form handling
            pass
    
    # GET request
    if is_ajax:
        members = Member.objects.all()
        data = list(members.values('id', 'firstname', 'lastname', 'email'))
        return JsonResponse({'members': data})
    else:
        # Return regular HTML
        return render(request, 'members/index.html', {'members': Member.objects.all()})
```

### Method 2: Separate AJAX Views

Better practice: Create dedicated API endpoints

```python
# members/views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

# List all members (AJAX)
def member_list_json(request):
    members = Member.objects.all()
    data = [{
        'id': m.pk,
        'firstname': m.firstname,
        'lastname': m.lastname,
        'email': m.email,
        'phone': m.phone
    } for m in members]
    return JsonResponse({'members': data})

# Get single member (AJAX)
def member_detail_json(request, pk):
    try:
        member = Member.objects.get(pk=pk)
        data = {
            'id': member.pk,
            'firstname': member.firstname,
            'lastname': member.lastname,
            'email': member.email,
            'phone': member.phone
        }
        return JsonResponse({'member': data})
    except Member.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)

# Create member (AJAX)
@require_http_methods(["POST"])
def member_create_json(request):
    try:
        data = json.loads(request.body)
        member = Member.objects.create(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            phone=data.get('phone', '')
        )
        return JsonResponse({
            'success': True,
            'member': {
                'id': member.pk,
                'firstname': member.firstname,
                'lastname': member.lastname,
                'email': member.email
            }
        }, status=201)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Update member (AJAX)
@require_http_methods(["POST", "PUT", "PATCH"])
def member_update_json(request, pk):
    try:
        member = Member.objects.get(pk=pk)
        data = json.loads(request.body)
        
        member.firstname = data.get('firstname', member.firstname)
        member.lastname = data.get('lastname', member.lastname)
        member.email = data.get('email', member.email)
        member.phone = data.get('phone', member.phone)
        member.save()
        
        return JsonResponse({
            'success': True,
            'member': {
                'id': member.pk,
                'firstname': member.firstname,
                'lastname': member.lastname,
                'email': member.email
            }
        })
    except Member.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Delete member (AJAX)
@require_http_methods(["POST", "DELETE"])
def member_delete_json(request, pk):
    try:
        member = Member.objects.get(pk=pk)
        member_data = {'id': member.pk, 'name': str(member)}
        member.delete()
        return JsonResponse({
            'success': True,
            'deleted': member_data
        })
    except Member.DoesNotExist:
        return JsonResponse({'error': 'Member not found'}, status=404)
```

```python
# members/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Regular HTML views
    path('', views.member_list, name='member_list'),
    path('<int:pk>/', views.member_detail, name='member_detail'),
    path('new/', views.member_create, name='member_create'),
    path('<int:pk>/edit/', views.member_update, name='member_update'),
    path('<int:pk>/delete/', views.member_delete, name='member_delete'),
    
    # AJAX/JSON API endpoints
    path('api/members/', views.member_list_json, name='member_list_json'),
    path('api/members/<int:pk>/', views.member_detail_json, name='member_detail_json'),
    path('api/members/create/', views.member_create_json, name='member_create_json'),
    path('api/members/<int:pk>/update/', views.member_update_json, name='member_update_json'),
    path('api/members/<int:pk>/delete/', views.member_delete_json, name='member_delete_json'),
]
```

### Frontend JavaScript Example

```html
<!-- templates/members/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Members</title>
</head>
<body>
    <h1>Members</h1>
    <button id="loadMembers">Load Members (AJAX)</button>
    <div id="memberList"></div>
    
    <h2>Add Member</h2>
    <form id="memberForm">
        {% csrf_token %}
        <input type="text" name="firstname" placeholder="First Name" required>
        <input type="text" name="lastname" placeholder="Last Name" required>
        <input type="email" name="email" placeholder="Email" required>
        <button type="submit">Add Member</button>
    </form>
    
    <script>
        // Get CSRF token
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        const csrftoken = getCookie('csrftoken');
        
        // Load members via AJAX
        document.getElementById('loadMembers').addEventListener('click', function() {
            fetch('/members/api/members/')
                .then(response => response.json())
                .then(data => {
                    const memberList = document.getElementById('memberList');
                    memberList.innerHTML = '<ul>' + 
                        data.members.map(m => 
                            `<li>${m.firstname} ${m.lastname} - ${m.email} 
                            <button onclick="deleteMember(${m.id})">Delete</button></li>`
                        ).join('') + 
                    '</ul>';
                })
                .catch(error => console.error('Error:', error));
        });
        
        // Create member via AJAX
        document.getElementById('memberForm').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = {
                firstname: this.firstname.value,
                lastname: this.lastname.value,
                email: this.email.value
            };
            
            fetch('/members/api/members/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Member created: ' + data.member.firstname);
                    this.reset();
                    document.getElementById('loadMembers').click(); // Reload list
                }
            })
            .catch(error => console.error('Error:', error));
        });
        
        // Delete member via AJAX
        function deleteMember(id) {
            if (!confirm('Are you sure?')) return;
            
            fetch(`/members/api/members/${id}/delete/`, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Member deleted');
                    document.getElementById('loadMembers').click(); // Reload list
                }
            })
            .catch(error => console.error('Error:', error));
        }
        
        // Update member via AJAX
        function updateMember(id, updateData) {
            fetch(`/members/api/members/${id}/update/`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify(updateData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Member updated');
                }
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
```

### Method 3: Using Django REST Framework (Recommended for APIs)

For serious API development, use Django REST Framework (DRF) - similar to Rails API mode.

```bash
pip install djangorestframework
```

```python
# settings.py
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'members',
]
```

```python
# members/serializers.py
from rest_framework import serializers
from .models import Member

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ['id', 'firstname', 'lastname', 'email', 'phone', 'joined_date']
        read_only_fields = ['id', 'joined_date']
```

```python
# members/views.py
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Member
from .serializers import MemberSerializer

# ViewSet (like Rails scaffold)
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    # Automatically provides: list, create, retrieve, update, destroy

# Or individual API views
@api_view(['GET', 'POST'])
def member_list_api(request):
    if request.method == 'GET':
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

```python
# members/urls.py (DRF)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Automatic routing (like Rails resources :members)
router = DefaultRouter()
router.register(r'members', views.MemberViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

# This creates:
# GET    /api/members/          -> list
# POST   /api/members/          -> create
# GET    /api/members/{id}/     -> retrieve
# PUT    /api/members/{id}/     -> update
# PATCH  /api/members/{id}/     -> partial_update
# DELETE /api/members/{id}/     -> destroy
```

### AJAX Comparison: Rails vs Django

| Feature | Rails | Django |
|---------|-------|--------|
| **Detect AJAX** | `request.xhr?` | `request.headers.get('X-Requested-With') == 'XMLHttpRequest'` |
| **Respond JSON** | `respond_to { \|format\| format.json }` | `return JsonResponse(data)` |
| **CSRF Token** | Auto in meta tags | Manual: `{% csrf_token %}` or get from cookie |
| **Parse JSON** | `params` (auto-parsed) | `json.loads(request.body)` |
| **Return Data** | `render json: @member` | `JsonResponse({'member': data})` |
| **REST Framework** | Built-in (Rails API) | Django REST Framework (install) |
| **Serializers** | Active Model Serializers | DRF Serializers |

### Important AJAX Notes

1. **CSRF Protection**: Always include CSRF token in AJAX requests
   ```javascript
   headers: {
       'X-CSRFToken': csrftoken
   }
   ```

2. **Content Type**: Set appropriate headers
   ```javascript
   headers: {
       'Content-Type': 'application/json'
   }
   ```

3. **HTTP Methods**: Django can handle any method, but forms typically use GET/POST
   - Use `@require_http_methods(["GET", "POST", "PUT", "DELETE"])` decorator

4. **Error Handling**: Return appropriate status codes
   ```python
   return JsonResponse({'error': 'Not found'}, status=404)
   ```

5. **CORS**: For cross-origin requests, use `django-cors-headers`
   ```bash
   pip install django-cors-headers
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

