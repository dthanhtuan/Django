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

Read in this order:

1. **[01-DJANGO-FOR-RAILS-DEVELOPERS.md](docs/01-DJANGO-FOR-RAILS-DEVELOPERS.md)** - Complete Django guide
2. **[02-MODELS-FORMS-ADMIN.md](docs/02-MODELS-FORMS-ADMIN.md)** - Models, Forms, Admin deep dive
3. **[03-GETTING-STARTED.md](docs/03-GETTING-STARTED.md)** - Quick start & practical guide

See [docs/README.md](docs/README.md) for the complete documentation index.

---

## ✨ Features

- ✅ Complete CRUD operations (Create, Read, Update, Delete)
- ✅ AJAX/JSON API endpoints
- ✅ Django Admin interface (fully configured)
- ✅ Form validation and error handling
- ✅ Bootstrap-ready templates
- ✅ Flash messages
- ✅ Test data included (8 members)

---

## 📁 Project Structure

```
my_tennis_club/
├── docs/                          # Complete documentation
│   ├── README.md                  # Documentation index
│   ├── 01-DJANGO-FOR-RAILS-DEVELOPERS.md
│   ├── 02-MODELS-FORMS-ADMIN.md
│   └── 03-GETTING-STARTED.md
│
├── members/                       # Members app
│   ├── models.py                  # Member model
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

✅ Django project structure  
✅ Models with Meta class  
✅ Forms and validation  
✅ CRUD operations  
✅ AJAX handling  
✅ Admin interface  
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

