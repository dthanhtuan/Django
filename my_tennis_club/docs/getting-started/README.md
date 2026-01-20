# Getting Started with Django

This section contains introductory guides to help you start learning Django coming from a Rails background.

## Documents in This Section

### [Django for Rails Developers](01-DJANGO-FOR-RAILS-DEVELOPERS.md)
**The main guide** - Start here for a comprehensive introduction to Django

**What's covered:**
- Django vs Rails comparison table
- Core concepts (Projects vs Apps, MVT pattern)
- Project structure explained
- How Django loads files
- Complete CRUD operations guide
- AJAX handling in Django
- Common tasks comparison
- Key differences to remember

**Reading time:** 30-60 minutes

---

### [Quick Start Guide](03-GETTING-STARTED.md)
**Hands-on practice** - Get the tennis club app running

**What's covered:**
- 3 steps to run the application
- Testing CRUD and AJAX features
- CRUD operations quick reference
- Common Django commands
- Troubleshooting common issues

**Reading time:** 15-20 minutes

---

## Recommended Reading Order

1. **Start with:** [Django for Rails Developers](01-DJANGO-FOR-RAILS-DEVELOPERS.md)
   - Read the entire guide to understand Django's fundamentals
   - Pay special attention to the Django vs Rails comparison sections

2. **Then practice with:** [Quick Start Guide](03-GETTING-STARTED.md)
   - Get hands-on experience running the application
   - Test the features you just learned about
   - Familiarize yourself with Django commands

3. **Next, explore:**
   - [Model Relationships](../relationships/) - Understand Django's relationship patterns
   - [ORM Queries](../orm-queries/) - Learn how to query data
   - [Advanced Topics](../advanced/) - Dive deeper into forms and admin

---

## Quick Reference

**Start the server:**
```bash
python manage.py runserver
```

**Create admin user:**
```bash
python manage.py createsuperuser
```

**Access the application:**
- Members list: http://localhost:8000/members/
- Admin panel: http://localhost:8000/admin/

---

[← Back to Documentation Home](../README.md)

