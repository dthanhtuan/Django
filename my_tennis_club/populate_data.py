"""
Script to populate test data for the Tennis Club members.
Run with: python manage.py shell < populate_data.py
Or: python manage.py shell
>>> exec(open('populate_data.py').read())
"""

from members.models import Member

# Clear existing data (optional)
print("Clearing existing members...")
Member.objects.all().delete()

# Create test members
print("Creating test members...")

members_data = [
    {
        'firstname': 'Serena',
        'lastname': 'Williams',
        'email': 'serena.williams@tennis.com',
        'phone': '555-0101'
    },
    {
        'firstname': 'Roger',
        'lastname': 'Federer',
        'email': 'roger.federer@tennis.com',
        'phone': '555-0102'
    },
    {
        'firstname': 'Rafael',
        'lastname': 'Nadal',
        'email': 'rafael.nadal@tennis.com',
        'phone': '555-0103'
    },
    {
        'firstname': 'Naomi',
        'lastname': 'Osaka',
        'email': 'naomi.osaka@tennis.com',
        'phone': '555-0104'
    },
    {
        'firstname': 'Novak',
        'lastname': 'Djokovic',
        'email': 'novak.djokovic@tennis.com',
        'phone': '555-0105'
    },
    {
        'firstname': 'Simona',
        'lastname': 'Halep',
        'email': 'simona.halep@tennis.com',
        'phone': '555-0106'
    },
    {
        'firstname': 'Andy',
        'lastname': 'Murray',
        'email': 'andy.murray@tennis.com',
        'phone': '555-0107'
    },
    {
        'firstname': 'Maria',
        'lastname': 'Sharapova',
        'email': 'maria.sharapova@tennis.com',
        'phone': '555-0108'
    },
]

for data in members_data:
    member = Member.objects.create(**data)
    print(f"✅ Created: {member}")

print(f"\n🎾 Successfully created {Member.objects.count()} members!")
print("\nYou can now:")
print("1. Visit http://localhost:8000/members/ to see them")
print("2. Visit http://localhost:8000/admin/ to manage them")
print("3. Test AJAX at http://localhost:8000/members/ (scroll to AJAX Demo section)")

