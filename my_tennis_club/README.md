# 🎾 Django Tennis Club

A complete Django CRUD application with AJAX support, built as a learning resource for Rails developers transitioning to Django.

---

## 🚀 Quick Start

```bash
# 1. Start the server
python manage.py runserver

# 2. Visit in browser
# http://localhost:8000/members/

# 3. Create admin user (optional)
python manage.py createsuperuser
# Then visit: http://localhost:8000/admin/
```

---

## 📚 Documentation

**All documentation is in the [`docs/`](docs/) folder.**

### Quick Links

1. **[01-DJANGO-FOR-RAILS-DEVELOPERS.md](docs/01-DJANGO-FOR-RAILS-DEVELOPERS.md)** ⭐ START HERE
   - Complete Django guide for Rails developers
   - Django vs Rails comparison
   - CRUD operations & AJAX handling

2. **[RELATIONSHIPS-GUIDE.md](docs/RELATIONSHIPS-GUIDE.md)** ⭐ IMPORTANT
   - Model relationships (belongs_to, has_one, has_many)
   - ForeignKey, OneToOneField, ManyToManyField
   - Working examples with Team, Member, Profile models

3. **[02-MODELS-FORMS-ADMIN.md](docs/02-MODELS-FORMS-ADMIN.md)**
   - Models, Forms, Admin deep dive
   - Meta class explained
   - Visual diagrams

4. **[03-GETTING-STARTED.md](docs/03-GETTING-STARTED.md)**
   - Quick start & practical guide
   - Testing CRUD and AJAX

**See [docs/README.md](docs/README.md) for the complete documentation guide.**

---

## ✨ Features

**CRUD & AJAX:**
- ✅ Complete CRUD operations (NEW, EDIT, INDEX, UPDATE, DELETE, CREATE)
- ✅ AJAX/JSON API endpoints
- ✅ Form validation and error handling
- ✅ Bootstrap-ready templates
- ✅ Flash messages

**Model Relationships:**
- ✅ **belongs_to** - Member belongs to Team (ForeignKey)
- ✅ **has_one** - Member has one Profile (OneToOneField)
- ✅ **has_many** - Team has many Members (reverse ForeignKey)

**Admin Panel:**
- ✅ Django Admin interface (fully configured)
- ✅ Custom admin for Team, Member, Profile
- ✅ Search, filters, and inline editing

**Data:**
- ✅ Test data included (Teams, Members, Profiles)
- ✅ Migration files included

---

## 📁 Project Structure

```
my_tennis_club/
├── docs/                          # Complete documentation
│   ├── README.md                  # Documentation index
│   ├── 01-DJANGO-FOR-RAILS-DEVELOPERS.md    # Django for Rails devs
│   ├── 02-MODELS-FORMS-ADMIN.md              # Models, Forms, Admin
│   ├── 03-GETTING-STARTED.md                 # Quick start guide
│   └── RELATIONSHIPS-GUIDE.md                # Model relationships ⭐
│
├── members/                       # Members app
│   ├── models.py                  # Team, Member, Profile models
│   ├── forms.py                   # MemberForm
│   ├── views.py                   # CRUD + AJAX views
│   ├── urls.py                    # URL patterns
│   ├── admin.py                   # Admin configuration
│   └── templates/members/         # HTML templates
│
├── my_tennis_club/                # Project settings
│   ├── settings.py                # Configuration
│   └── urls.py                    # Root URL config
│
├── manage.py                      # Django CLI
├── db.sqlite3                     # SQLite database
└── populate_data.py               # Test data script
```

---

## 🎯 Key Concepts (Django vs Rails)

| Aspect | Rails | Django |
|--------|-------|--------|
| **Pattern** | MVC | MVT (Model-View-Template) |
| **Routing** | `resources :members` | Explicit URL patterns |
| **Controllers** | `app/controllers/` | Views (`views.py`) |
| **Views** | ERB templates | Django Templates |
| **Admin** | ActiveAdmin (gem) | Built-in |
| **Forms** | View helpers | Form classes |

**Key Difference:** Django "Views" = Rails "Controllers"!

---

## 💡 Common Commands

```bash
# Development
python manage.py runserver              # Start server
python manage.py shell                  # Interactive shell

# Database
python manage.py makemigrations         # Create migrations
python manage.py migrate                # Apply migrations

# Admin
python manage.py createsuperuser        # Create admin user

# Testing
python manage.py check                  # Check for errors
python manage.py test                   # Run tests
```

---

## 📖 Learning Resources

- **Documentation**: See [`docs/`](docs/) folder
- **Django Docs**: https://docs.djangoproject.com/
- **Django Tutorial**: https://docs.djangoproject.com/en/stable/intro/tutorial01/

---

## 🎓 What You'll Learn

**Core Django:**
✅ Django project structure  
✅ Projects vs Apps concept  
✅ MVT pattern (Models, Views, Templates)  
✅ How Django loads files  

**CRUD & Forms:**
✅ Complete CRUD operations (NEW, EDIT, INDEX, UPDATE, DELETE, CREATE)  
✅ AJAX handling  
✅ Forms and validation  

**Model Relationships:**
✅ belongs_to (ForeignKey)  
✅ has_one (OneToOneField)  
✅ has_many (reverse ForeignKey)  
✅ has_many :through (ManyToManyField)  

**Admin & More:**
✅ Models with Meta class  
✅ Admin interface customization  
✅ URL routing  
✅ Templates  

---

## 🌐 URLs

Once the server is running:

- **Members List**: http://localhost:8000/members/
- **New Member**: http://localhost:8000/members/new/
- **Admin Panel**: http://localhost:8000/admin/
- **API (JSON)**: http://localhost:8000/members/api/members/

---

## 📝 Database

The project includes test data with 8 famous tennis players:
- Serena Williams
- Roger Federer
- Rafael Nadal
- Naomi Osaka
- Novak Djokovic
- Simona Halep
- Andy Murray
- Maria Sharapova

To reset/repopulate:
```bash
python manage.py shell < populate_data.py
```

---

## 🛠️ Requirements

- Python 3.8+
- Django 6.0+
- SQLite (included with Python)

---

## 📄 License

This is a learning project. Feel free to use and modify.

---

**Happy coding! 🎾🐍**

For detailed documentation, see the [`docs/`](docs/) folder.

