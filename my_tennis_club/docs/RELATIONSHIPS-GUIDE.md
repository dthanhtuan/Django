# Django Model Relationships - Complete Guide

A comprehensive guide to Django model relationships (Foreign Keys, One-to-One, Many-to-Many) compared to Rails ActiveRecord associations.

---

## 📋 Quick Summary

**What's in this project:** This Tennis Club application now demonstrates all major Django relationship types:

- ✅ **Team** model (has_many members)
- ✅ **Member** model (belongs_to team, has_one profile)
- ✅ **Profile** model (belongs_to member)

### Models Created

```python
# Team - has_many members
class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)

# Member - belongs_to team, has_one profile
class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members', null=True, blank=True)

# Profile - belongs_to member (creates has_one)
class Profile(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    skill_level = models.CharField(max_length=20, choices=[...])
    favorite_surface = models.CharField(max_length=20, choices=[...])
```

### Relationship Diagram

```
Team (has_many)
  ↓
  ├── Member 1 (belongs_to team, has_one profile)
  │     └── Profile 1 (belongs_to member)
  ├── Member 2
  │     └── Profile 2
  └── Member 3
        └── Profile 3
```

### Quick Usage Examples

```python
# Create team
team = Team.objects.create(name="Red Team")

# Create member with team (belongs_to)
member = Member.objects.create(firstname="John", lastname="Doe", email="john@example.com", team=team)

# Create profile (has_one)
profile = Profile.objects.create(member=member, bio="Expert player", skill_level="advanced")

# Query relationships
print(member.team.name)           # belongs_to → "Red Team"
print(member.profile.skill_level) # has_one → "advanced"
print(team.members.count())       # has_many → 1
```

### Test in Django Shell

```bash
python manage.py shell
```

```python
from members.models import Team, Member, Profile

# Try the examples above!
```

---

## Table of Contents
- [Quick Summary](#quick-summary) ⭐ You are here
- [Overview: Rails vs Django](#overview-rails-vs-django)
- [belongs_to (Many-to-One)](#belongs_to-many-to-one)
- [has_one (One-to-One)](#has_one-one-to-one)
- [has_many (reverse of ForeignKey)](#has_many-reverse-of-foreignkey)
- [has_many :through (Many-to-Many)](#has_many-through-many-to-many)
- [Querying Relationships](#querying-relationships)
- [Examples in Your Project](#examples-in-your-project)

---

## Overview: Rails vs Django

| Rails Association | Django Field | Relationship Type |
|-------------------|--------------|-------------------|
| `belongs_to` | `ForeignKey` | Many-to-One |
| `has_one` | Reverse of `OneToOneField` | One-to-One |
| `has_many` | Reverse of `ForeignKey` | One-to-Many |
| `has_many :through` | `ManyToManyField` | Many-to-Many |

---

## belongs_to (Many-to-One)

### Rails
```ruby
class Member < ApplicationRecord
  belongs_to :team
end

class Team < ApplicationRecord
  has_many :members
end
```

### Django
```python
class Team(models.Model):
    name = models.CharField(max_length=255)

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    
    # belongs_to :team
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,  # What to do when team is deleted
        related_name='members',     # Reverse relation name (team.members)
        null=True,                  # Optional relationship
        blank=True                  # Optional in forms
    )
```

### on_delete Options

**IMPORTANT:** Django requires you to specify what happens when the related object is deleted.

```python
# CASCADE - Delete member when team is deleted (like dependent: :destroy)
on_delete=models.CASCADE

# PROTECT - Prevent team deletion if it has members (like dependent: :restrict_with_error)
on_delete=models.PROTECT

# SET_NULL - Set member.team to NULL when team is deleted
on_delete=models.SET_NULL  # requires null=True

# SET_DEFAULT - Set to default value
on_delete=models.SET_DEFAULT  # requires default=...

# DO_NOTHING - Do nothing (dangerous!)
on_delete=models.DO_NOTHING
```

**Rails equivalent:**
```ruby
belongs_to :team, dependent: :destroy   # CASCADE
belongs_to :team, dependent: :restrict  # PROTECT
belongs_to :team, optional: true        # null=True
```

### Usage

```python
# Create team
team = Team.objects.create(name="Red Team")

# Create member with team
member = Member.objects.create(
    firstname="John",
    team=team
)

# Access team from member (belongs_to)
print(member.team.name)  # "Red Team"

# Access members from team (has_many - reverse relation)
for member in team.members.all():
    print(member.firstname)
```

---

## has_one (One-to-One)

Each Member has ONE Profile, each Profile belongs to ONE Member.

### Rails
```ruby
class Member < ApplicationRecord
  has_one :profile
end

class Profile < ApplicationRecord
  belongs_to :member
end
```

### Django
```python
class Member(models.Model):
    firstname = models.CharField(max_length=255)

class Profile(models.Model):
    # This creates both sides of the relationship
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name='profile'  # Allows: member.profile
    )
    bio = models.TextField(blank=True)
    skill_level = models.CharField(max_length=20)
```

**Key Point:** In Django, you define `OneToOneField` on the "belongs_to" side (Profile), but it creates a reverse relationship automatically.

### Usage

```python
# Create member
member = Member.objects.create(firstname="John")

# Create profile for member
profile = Profile.objects.create(
    member=member,
    bio="Expert tennis player",
    skill_level="advanced"
)

# Access profile from member (has_one)
print(member.profile.bio)  # "Expert tennis player"

# Access member from profile (belongs_to)
print(profile.member.firstname)  # "John"

# Check if profile exists
if hasattr(member, 'profile'):
    print("Profile exists")
```

### Difference from ForeignKey

```python
# ForeignKey - Many members can have same team (Many-to-One)
team = models.ForeignKey(Team, ...)

# OneToOneField - Only ONE profile per member (One-to-One)
member = models.OneToOneField(Member, ...)
```

---

## has_many (Reverse of ForeignKey)

This is the **reverse** of `belongs_to`. Django automatically creates this relationship.

### Rails
```ruby
class Team < ApplicationRecord
  has_many :members
end

class Member < ApplicationRecord
  belongs_to :team
end
```

### Django
```python
class Team(models.Model):
    name = models.CharField(max_length=255)
    # No explicit has_many field needed!

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    
    # This ForeignKey automatically creates team.members
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members'  # ← This is the has_many accessor
    )
```

**Note:** Django automatically creates the reverse relationship. You control the name with `related_name`.

### related_name Options

```python
# Custom name
team = models.ForeignKey(Team, related_name='members')
# Usage: team.members.all()

# Default name (if related_name not specified)
team = models.ForeignKey(Team, on_delete=models.CASCADE)
# Usage: team.member_set.all()  # Note the _set suffix

# Disable reverse relation
team = models.ForeignKey(Team, related_name='+', on_delete=models.CASCADE)
# No reverse relation created
```

### Usage

```python
# Get all members of a team (has_many)
team = Team.objects.get(name="Red Team")
members = team.members.all()

# Filter members
advanced_members = team.members.filter(skill_level='advanced')

# Count members
count = team.members.count()

# Add member to team
member = Member.objects.create(firstname="Jane")
team.members.add(member)

# Remove member from team
team.members.remove(member)

# Clear all members
team.members.clear()
```

**Rails equivalent:**
```ruby
team = Team.find_by(name: "Red Team")
members = team.members

advanced_members = team.members.where(skill_level: 'advanced')
count = team.members.count

team.members << member
team.members.delete(member)
team.members.clear
```

---

## has_many :through (Many-to-Many)

Members can belong to multiple Teams, Teams can have multiple Members.

### Rails
```ruby
class Member < ApplicationRecord
  has_many :team_memberships
  has_many :teams, through: :team_memberships
end

class Team < ApplicationRecord
  has_many :team_memberships
  has_many :members, through: :team_memberships
end

class TeamMembership < ApplicationRecord
  belongs_to :member
  belongs_to :team
end
```

### Django - Method 1: Simple ManyToManyField

```python
class Team(models.Model):
    name = models.CharField(max_length=255)

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    
    # Simple many-to-many (no extra fields)
    teams = models.ManyToManyField(
        Team,
        related_name='members',
        blank=True
    )
```

**Usage:**
```python
# Add member to team
member.teams.add(team)

# Add multiple teams
member.teams.add(team1, team2, team3)

# Remove team
member.teams.remove(team)

# Get all teams for member
teams = member.teams.all()

# Get all members for team (reverse)
members = team.members.all()
```

### Django - Method 2: Through Model (with extra fields)

```python
class Team(models.Model):
    name = models.CharField(max_length=255)

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    
    # Many-to-many with through model
    teams = models.ManyToManyField(
        Team,
        through='Membership',
        related_name='members'
    )

class Membership(models.Model):
    """Join table with extra fields"""
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    
    # Extra fields
    role = models.CharField(max_length=50)  # captain, player, coach
    joined_date = models.DateField(auto_now_add=True)
    
    class Meta:
        unique_together = ('member', 'team')  # Prevent duplicates
```

**Usage with through model:**
```python
# Can't use .add() directly with through model
# Must create Membership explicitly
membership = Membership.objects.create(
    member=member,
    team=team,
    role='captain'
)

# Query
member.teams.all()  # All teams
team.members.all()  # All members

# Access through data
memberships = member.membership_set.all()
for m in memberships:
    print(f"{m.team.name} - {m.role}")
```

---

## Querying Relationships

### Forward Queries (Following the ForeignKey)

```python
# Get member's team
member = Member.objects.get(id=1)
team = member.team

# Filter members by team
members = Member.objects.filter(team__name='Red Team')

# Filter members by team property
members = Member.objects.filter(team__created_date__year=2024)
```

**Rails equivalent:**
```ruby
member = Member.find(1)
team = member.team

members = Member.where(team: { name: 'Red Team' }).joins(:team)
```

### Reverse Queries (Following the reverse relation)

```python
# Get team's members
team = Team.objects.get(name='Red Team')
members = team.members.all()

# Filter teams by member count
teams = Team.objects.annotate(
    member_count=Count('members')
).filter(member_count__gt=5)

# Filter teams that have a specific member
teams = Team.objects.filter(members__firstname='John')
```

**Rails equivalent:**
```ruby
team = Team.find_by(name: 'Red Team')
members = team.members

teams = Team.joins(:members).group(:id).having('COUNT(members.id) > ?', 5)
teams = Team.joins(:members).where(members: { firstname: 'John' })
```

### Select Related (Eager Loading)

```python
# N+1 problem - BAD
members = Member.objects.all()
for member in members:
    print(member.team.name)  # Queries database for each member!

# Solution: select_related (for ForeignKey, OneToOne)
members = Member.objects.select_related('team').all()
for member in members:
    print(member.team.name)  # No extra queries!

# prefetch_related (for reverse ForeignKey, ManyToMany)
teams = Team.objects.prefetch_related('members').all()
for team in teams:
    for member in team.members.all():  # No extra queries!
        print(member.firstname)
```

**Rails equivalent:**
```ruby
# includes (eager loading)
members = Member.includes(:team)
teams = Team.includes(:members)
```

---

## Examples in Your Project

### Your Current Models

```python
# Team Model (has_many members)
class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)

# Member Model (belongs_to team, has_one profile)
class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    
    # belongs_to :team
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members',
        null=True,
        blank=True
    )

# Profile Model (belongs_to member - creating has_one)
class Profile(models.Model):
    # This creates member.profile (has_one)
    member = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True)
    skill_level = models.CharField(max_length=20)
```

### Usage Examples

```python
# Create team
team = Team.objects.create(name="Red Team", description="Advanced players")

# Create member with team (belongs_to)
member = Member.objects.create(
    firstname="John",
    lastname="Doe",
    email="john@example.com",
    team=team
)

# Create profile for member (has_one)
profile = Profile.objects.create(
    member=member,
    bio="Expert player",
    skill_level="advanced"
)

# Access relationships
print(member.team.name)           # "Red Team" (belongs_to)
print(member.profile.skill_level) # "advanced" (has_one)
print(team.members.count())       # 1 (has_many)

# Query with relationships
# Get all advanced members on Red Team
advanced_red = Member.objects.filter(
    team__name='Red Team',
    profile__skill_level='advanced'
)

# Get teams with more than 5 members
from django.db.models import Count
big_teams = Team.objects.annotate(
    num_members=Count('members')
).filter(num_members__gt=5)
```

---

## Comparison Table

| Operation | Rails | Django |
|-----------|-------|--------|
| **Define belongs_to** | `belongs_to :team` | `team = models.ForeignKey(Team, ...)` |
| **Define has_one** | `has_one :profile` | Profile has `OneToOneField` to Member |
| **Define has_many** | `has_many :members` | Automatic via `related_name='members'` |
| **Define many-to-many** | `has_many :through` | `ManyToManyField` or `through=` |
| **Access forward** | `member.team` | `member.team` |
| **Access reverse** | `team.members` | `team.members.all()` |
| **Add to collection** | `team.members << member` | `team.members.add(member)` |
| **Remove from collection** | `team.members.delete(member)` | `team.members.remove(member)` |
| **Count** | `team.members.count` | `team.members.count()` |
| **Filter** | `team.members.where(...)` | `team.members.filter(...)` |
| **Eager loading** | `includes(:team)` | `select_related('team')` |
| **Eager loading reverse** | `includes(:members)` | `prefetch_related('members')` |

---

## Best Practices

### 1. Always Specify on_delete

```python
# ✅ GOOD
team = models.ForeignKey(Team, on_delete=models.CASCADE)

# ❌ BAD (will raise error in Django)
team = models.ForeignKey(Team)
```

### 2. Use related_name

```python
# ✅ GOOD - Clear and readable
team = models.ForeignKey(Team, related_name='members', ...)
# Usage: team.members.all()

# ❌ OKAY but less clear
team = models.ForeignKey(Team, on_delete=models.CASCADE)
# Usage: team.member_set.all()  # _set suffix is confusing
```

### 3. Use select_related for Performance

```python
# ✅ GOOD - One query
members = Member.objects.select_related('team').all()

# ❌ BAD - N+1 queries
members = Member.objects.all()
for member in members:
    print(member.team.name)  # Separate query for each!
```

### 4. Null vs Blank

```python
# null=True → Database allows NULL
# blank=True → Forms allow empty value

# Optional team (can be None)
team = models.ForeignKey(Team, null=True, blank=True, ...)

# Required team
team = models.ForeignKey(Team, on_delete=models.CASCADE)
```

---

## Quick Reference

### Create Relationships

```python
# belongs_to (Many-to-One)
field = models.ForeignKey(OtherModel, on_delete=models.CASCADE, related_name='items')

# has_one (One-to-One)
field = models.OneToOneField(OtherModel, on_delete=models.CASCADE, related_name='detail')

# has_many (reverse of ForeignKey)
# Defined automatically via related_name

# has_many :through (Many-to-Many)
field = models.ManyToManyField(OtherModel, related_name='items')
# or with through model:
field = models.ManyToManyField(OtherModel, through='ThroughModel', related_name='items')
```

---

**Happy modeling! 🎾🐍**

