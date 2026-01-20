# 🎾 Django Tennis Club

A complete Django learning project designed specifically for **Rails developers** transitioning to Django. If you know Rails and want to learn Django, this project provides familiar concepts with clear comparisons and practical examples.

---

## 👋 For Rails Developers

This project assumes you're comfortable with Rails and uses that knowledge as a foundation. Every concept is explained in terms of Rails equivalents—from ActiveRecord to Django ORM, from `belongs_to` to ForeignKey, from controllers to views.

**What makes this different:**
- Every Django feature compared to its Rails equivalent
- Comprehensive guides written for Rails developers
- Same CRUD patterns you know, Django syntax you'll learn
- Clear explanations of what's the same and what's different

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

## 📚 Documentation for Rails Developers

**All documentation is organized by topic in the [`docs/`](docs/) folder.**

### 📖 Documentation Sections

**🚀 [Getting Started](docs/getting-started/)** - Begin your Django journey
- [Django for Rails Developers](docs/getting-started/01-DJANGO-FOR-RAILS-DEVELOPERS.md) - Main guide
- [Quick Start](docs/getting-started/03-GETTING-STARTED.md) - Get the app running

**🔗 [Relationships](docs/relationships/)** - Understanding Django relationships  
- [Django vs Rails Relationships](docs/relationships/DJANGO-VS-RAILS-RELATIONSHIPS.md) 🚨 **Read this first!**
- [Complete Relationships Guide](docs/relationships/RELATIONSHIPS-GUIDE.md)
- [Multiple ForeignKeys Pattern](docs/relationships/MULTIPLE-FOREIGNKEYS-SAME-MODEL.md)

**📊 [ORM & Queries](docs/orm-queries/)** - Querying data
- [Django ORM vs Rails Active Record](docs/orm-queries/DJANGO-ORM-VS-RAILS-ACTIVE-RECORD.md) - Complete comparison

**🎓 [Advanced Topics](docs/advanced/)** - Deep dive
- [Models, Forms & Admin](docs/advanced/02-MODELS-FORMS-ADMIN.md) - Meta class, forms, admin

### Quick Links

| I Want To... | Read This |
|-------------|-----------|
| **Start learning Django** | [Django for Rails Developers](docs/getting-started/01-DJANGO-FOR-RAILS-DEVELOPERS.md) |
| **Understand the #1 difference** | [Django vs Rails Relationships](docs/relationships/DJANGO-VS-RAILS-RELATIONSHIPS.md) |
| **Run the app now** | [Quick Start Guide](docs/getting-started/03-GETTING-STARTED.md) |
| **Translate a Rails query** | [ORM Comparison](docs/orm-queries/DJANGO-ORM-VS-RAILS-ACTIVE-RECORD.md) |
| **Learn all relationship types** | [Relationships Guide](docs/relationships/RELATIONSHIPS-GUIDE.md) |

**See [docs/README.md](docs/README.md) for the complete documentation index and learning paths.**

---

## ✨ What This Project Demonstrates

**Everything explained with Rails comparisons:**

**CRUD & AJAX (Just Like Rails, Different Syntax):**
- ✅ Complete CRUD operations (NEW, EDIT, INDEX, UPDATE, DELETE, CREATE)
- ✅ AJAX/JSON API endpoints (Django's approach vs Rails UJS)
- ✅ Form validation and error handling (Form classes vs Rails helpers)
- ✅ Bootstrap-ready templates
- ✅ Flash messages (Django's `messages` framework)

**Model Relationships (The Big Difference!):**
- ✅ **belongs_to** → ForeignKey (Member belongs to Team)
- ✅ **has_one** → OneToOneField (Member has one Profile)
- ✅ **has_many** → Reverse ForeignKey (Team has many Members)
- ✅ **has_many :through** → ManyToManyField (Member ↔ Tournaments)

**🔑 Key Insight:** In Django, you define each relationship on ONE side only. Rails requires both sides—Django creates the reverse automatically. This is explained in detail in the documentation.

**Admin Panel (Better Than ActiveAdmin):**
- ✅ Built-in admin interface (no gem installation needed!)
- ✅ Custom admin for Team, Member, Profile, Tournament
- ✅ Search, filters, and inline editing
- ✅ ManyToMany widget for tournament registration

**Database & Data:**
- ✅ Migrations work similarly to Rails migrations
- ✅ Test data included (8 tennis players)
- ✅ SQLite database (like Rails development default)

---

## 📁 Project Structure

```
my_tennis_club/
├── docs/                          # Complete documentation
│   ├── README.md                  # Documentation index
│   ├── DJANGO-VS-RAILS-RELATIONSHIPS.md  # 🚨 Critical differences
│   ├── 01-DJANGO-FOR-RAILS-DEVELOPERS.md # Django for Rails devs
│   ├── 02-MODELS-FORMS-ADMIN.md           # Models, Forms, Admin
│   ├── 03-GETTING-STARTED.md              # Quick start guide
│   └── RELATIONSHIPS-GUIDE.md             # Model relationships ⭐
│
├── members/                       # Members app
│   ├── models.py                  # Team, Member, Profile, Tournament models
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

**For Rails Developers:**
- **This Project's Documentation**: See [`docs/`](docs/) folder - everything compared to Rails
- **Official Django Tutorial**: https://docs.djangoproject.com/en/stable/intro/tutorial01/ (read after this project)
- **Django Docs**: https://docs.djangoproject.com/ (reference when needed)

**Learning Path:**
1. Start with this project's documentation (designed for Rails devs)
2. Build features on this project to practice
3. Read official Django docs for advanced topics

---

## 🎓 What You'll Learn (Coming from Rails)

**Core Django Concepts:**
✅ How Django projects differ from Rails apps  
✅ Projects vs Apps (Django's modular approach)  
✅ MVT pattern vs MVC (terminology flip!)  
✅ How Django loads and organizes files  

**CRUD & Forms (Rails Comparison):**
✅ Views = Controllers (terminology difference)  
✅ Templates = Views (HTML rendering)  
✅ Form classes vs Rails form helpers  
✅ AJAX handling without UJS  

**Database & ORM (ActiveRecord → Django ORM):**
✅ `User.where()` → `User.objects.filter()`  
✅ `belongs_to` → ForeignKey  
✅ `has_one` → OneToOneField  
✅ `has_many` → Reverse ForeignKey (automatic!)  
✅ `has_many :through` → ManyToManyField  
✅ `includes()` → `select_related()` / `prefetch_related()`  

**Admin & Tools:**
✅ Built-in admin vs ActiveAdmin gem  
✅ Meta class for model configuration  
✅ URL routing (explicit vs Rails magic)  
✅ Migration system (similar but different syntax)  

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

**Note:** This project is specifically designed as a Rails-to-Django learning resource. All documentation assumes Rails knowledge and uses it as the foundation for teaching Django concepts.

For detailed documentation with Rails comparisons throughout, see the [`docs/`](docs/) folder.

