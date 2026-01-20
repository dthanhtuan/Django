# Django Model Relationships: A Complete Guide

If you're coming from Rails, Django's approach to model relationships might seem strange at first. In Rails, you explicitly declare relationships on both sides—write `belongs_to :team` in Member and `has_many :members` in Team. Django takes a different approach: you define each relationship only once, and the framework creates the reverse relationship automatically.

This guide will walk you through all the relationship types Django offers and show you how they map to Rails associations you already know.

## Understanding the One-Side Definition Pattern

Let's address the elephant in the room: why does Django only require you to define relationships on one side?

In Rails, if a member belongs to a team, you write:

```ruby
class Member < ApplicationRecord
  belongs_to :team
end

class Team < ApplicationRecord
  has_many :members
end
```

Both sides are explicit. In Django, you only write:

```python
class Member(models.Model):
    team = models.ForeignKey(Team, related_name='members')

class Team(models.Model):
    pass  # That's it—no members field needed
```

The `related_name` parameter tells Django to create a `members` attribute on Team automatically. When you call `team.members.all()`, Django knows to look up all members where `member.team == team`.

This isn't just about saving keystrokes—it's about preventing inconsistencies. If you could define the relationship twice, you might accidentally give them different names or options, creating confusion. Django's approach ensures there's one source of truth.

## Your Tennis Club Models

The tennis club application demonstrates all the major relationship types. Here's what we're working with:

```python
class Tournament(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()

class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)

class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members', null=True, blank=True)
    tournaments = models.ManyToManyField(Tournament, related_name='members', blank=True)

class Profile(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    skill_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('professional', 'Professional'),
    ])
```

Notice that Tournament and Team have no explicit fields for their members, yet we can still query them. That's Django's automatic reverse relationships at work.

## Many-to-One: The ForeignKey

In Rails, when you have a many-to-one relationship (many members belong to one team), you use `belongs_to` on one side and `has_many` on the other. Django uses `ForeignKey` and creates the reverse automatically.

### How It Works

When you define a ForeignKey in the Member model:

```python
team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
```

Django does several things:
1. Creates a `team_id` column in the members table
2. Lets you access `member.team` to get the team object
3. Lets you access `team.members.all()` to get all members on that team

The `on_delete` parameter is required in Django. It tells the database what to do when a team is deleted. `CASCADE` means "delete all members on this team too"—like Rails' `dependent: :destroy`.

### Common on_delete Options

**CASCADE**: Delete related objects when the parent is deleted
```python
team = models.ForeignKey(Team, on_delete=models.CASCADE)
# Rails equivalent: belongs_to :team, dependent: :destroy
```

**PROTECT**: Prevent deletion if related objects exist
```python
team = models.ForeignKey(Team, on_delete=models.PROTECT)
# Rails equivalent: belongs_to :team, dependent: :restrict_with_error
```

**SET_NULL**: Set the foreign key to NULL when the parent is deleted
```python
team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
# Rails equivalent: No direct equivalent, but similar to dependent: :nullify
```

### Using ForeignKey Relationships

```python
# Create a team
team = Team.objects.create(name="Red Team", description="Advanced players")

# Create a member on that team
member = Member.objects.create(
    firstname="John",
    lastname="Doe",
    email="john@example.com",
    team=team
)

# Access the team from a member
print(member.team.name)  # "Red Team"

# Access members from a team (reverse relationship)
for member in team.members.all():
    print(f"{member.firstname} {member.lastname}")

# Count members on a team
print(team.members.count())

# Filter members
advanced_members = team.members.filter(profile__skill_level='advanced')
```

## One-to-One: The OneToOneField

A OneToOne relationship means each instance of one model corresponds to exactly one instance of another. Think user profiles: each user has exactly one profile, and each profile belongs to exactly one user.

In the tennis club, each member has one profile:

```python
class Profile(models.Model):
    member = models.OneToOneField(Member, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    skill_level = models.CharField(max_length=20)
```

The OneToOneField is defined in Profile, not Member. Why? Because Profile is the dependent model—it can't exist without a member. This mirrors where you'd put `belongs_to` in Rails.

### Using OneToOne Relationships

```python
# Create a member
member = Member.objects.create(
    firstname="Jane",
    lastname="Smith",
    email="jane@example.com"
)

# Create their profile
profile = Profile.objects.create(
    member=member,
    bio="Professional tennis player",
    skill_level="professional"
)

# Access the profile from the member
print(member.profile.bio)

# Access the member from the profile
print(profile.member.firstname)

# Handle missing profiles
try:
    bio = member.profile.bio
except Profile.DoesNotExist:
    bio = "No profile information available"
```

The key difference from ForeignKey is that OneToOneField ensures uniqueness. You can't create two profiles for the same member—Django will raise an error.

## One-to-Many: The Reverse Relationship

You might be wondering: where's the equivalent of Rails' `has_many`? The answer is: you don't need it. It's created automatically as the reverse of a ForeignKey.

When you write:

```python
class Member(models.Model):
    team = models.ForeignKey(Team, related_name='members')
```

Django creates `team.members` automatically. The `related_name` parameter specifies what to call it. If you don't specify `related_name`, Django uses the model name with `_set` appended: `team.member_set.all()`.

### Working with Reverse Relationships

```python
# Get all members on a team
team = Team.objects.get(name="Red Team")
members = team.members.all()

# Filter reverse relationships
beginner_members = team.members.filter(profile__skill_level='beginner')

# Count related objects
member_count = team.members.count()

# Check if any related objects exist
if team.members.exists():
    print("This team has members")

# Add objects to the relationship
new_member = Member.objects.create(firstname="Bob", lastname="Wilson")
team.members.add(new_member)

# Remove objects
team.members.remove(new_member)

# Clear all relationships
team.members.clear()
```

## Many-to-Many: The ManyToManyField

Many-to-many relationships are symmetric: members can participate in multiple tournaments, and tournaments can have multiple members. In Rails, you'd use `has_many :through` on both sides. In Django, you define `ManyToManyField` on one side (your choice), and Django creates both directions automatically.

```python
class Member(models.Model):
    tournaments = models.ManyToManyField(Tournament, related_name='members', blank=True)
```

We chose to define this in Member, but we could have defined it in Tournament instead. The result would be identical—Django creates a join table either way.

### Using ManyToMany Relationships

```python
# Create a tournament
us_open = Tournament.objects.create(
    name="US Open",
    location="New York",
    start_date="2026-08-31",
    end_date="2026-09-13"
)

# Get a member
member = Member.objects.first()

# Add the member to the tournament
member.tournaments.add(us_open)

# Access from the other side (even though Tournament has no tournaments field!)
participants = us_open.members.all()

# Add multiple tournaments at once
member.tournaments.add(wimbledon, french_open, australian_open)

# Remove from a tournament
member.tournaments.remove(us_open)

# Get all tournaments for a member
tournaments = member.tournaments.all()

# Check if a member is in a specific tournament
if us_open in member.tournaments.all():
    print("Member is participating in US Open")

# Clear all tournament registrations
member.tournaments.clear()
```

### ManyToMany with Extra Fields

Sometimes you need to store additional data about the relationship itself. For example, when a member registers for a tournament, you might want to track their registration date or seed number.

Django lets you specify a "through" model:

```python
class Member(models.Model):
    tournaments = models.ManyToManyField(
        Tournament,
        through='TournamentRegistration',
        related_name='members'
    )

class TournamentRegistration(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    seed_number = models.IntegerField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, default='pending')
    
    class Meta:
        unique_together = ('member', 'tournament')
```

When you use a through model, you can't use `.add()` directly. Instead, create the through model explicitly:

```python
# Create a registration
registration = TournamentRegistration.objects.create(
    member=member,
    tournament=us_open,
    seed_number=5,
    payment_status='paid'
)

# Query relationships still works
member.tournaments.all()
us_open.members.all()

# Access the through data
for registration in member.tournamentregistration_set.all():
    print(f"{registration.tournament.name} - Seed #{registration.seed_number}")
```

## Querying Across Relationships

Django lets you query across relationships using double underscores. This is incredibly powerful.

### Forward Queries (Following ForeignKeys)

```python
# Get all members on the "Red Team"
members = Member.objects.filter(team__name='Red Team')

# Get members whose team was created in 2026
members = Member.objects.filter(team__created_date__year=2026)

# Get members with advanced skill levels
members = Member.objects.filter(profile__skill_level='advanced')

# Chain multiple relationships
# Get members on Red Team with advanced skill level
members = Member.objects.filter(
    team__name='Red Team',
    profile__skill_level='advanced'
)
```

### Reverse Queries

```python
# Get teams that have at least one member
teams = Team.objects.filter(members__isnull=False).distinct()

# Get teams with more than 5 members
from django.db.models import Count
teams = Team.objects.annotate(
    member_count=Count('members')
).filter(member_count__gt=5)

# Get tournaments with at least one advanced player
tournaments = Tournament.objects.filter(
    members__profile__skill_level='advanced'
).distinct()
```

### Performance: select_related and prefetch_related

When you query across relationships, Django can make extra database queries—the N+1 problem Rails developers know well. Django provides two tools to optimize this:

**select_related** for forward ForeignKey and OneToOne:

```python
# BAD: Makes N+1 queries
members = Member.objects.all()
for member in members:
    print(member.team.name)  # Separate query for each team!

# GOOD: Makes one query with a JOIN
members = Member.objects.select_related('team').all()
for member in members:
    print(member.team.name)  # No extra queries!
```

**prefetch_related** for reverse ForeignKey and ManyToMany:

```python
# BAD: Makes N+1 queries
teams = Team.objects.all()
for team in teams:
    print(team.members.count())  # Separate query for each team!

# GOOD: Makes two queries total
teams = Team.objects.prefetch_related('members').all()
for team in teams:
    print(team.members.count())  # No extra queries!
```

In Rails, this is like using `includes`:

```ruby
# Rails
members = Member.includes(:team)
teams = Team.includes(:members)
```

## Practical Examples

Let's put it all together with realistic scenarios.

### Creating a Complete Member Record

```python
# Create a team
red_team = Team.objects.create(
    name="Red Team",
    description="Advanced competitive players"
)

# Create a tournament
wimbledon = Tournament.objects.create(
    name="Wimbledon",
    location="London",
    start_date="2026-06-22",
    end_date="2026-07-05"
)

# Create a member with a team
member = Member.objects.create(
    firstname="John",
    lastname="Doe",
    email="john.doe@example.com",
    team=red_team
)

# Create their profile
profile = Profile.objects.create(
    member=member,
    bio="Competitive tennis player specializing in grass courts",
    skill_level="advanced"
)

# Register for tournament
member.tournaments.add(wimbledon)

# Now all these work:
print(member.team.name)              # "Red Team"
print(member.profile.skill_level)    # "advanced"
print(member.tournaments.first().name) # "Wimbledon"
print(red_team.members.count())      # 1
print(wimbledon.members.count())     # 1
```

### Finding Related Data

```python
# Find all members on Red Team playing in Wimbledon
members = Member.objects.filter(
    team__name='Red Team',
    tournaments__name='Wimbledon'
)

# Find teams with at least one member in a tournament
teams_with_tournament_players = Team.objects.filter(
    members__tournaments__isnull=False
).distinct()

# Find advanced players on any team
advanced_members = Member.objects.filter(
    profile__skill_level='advanced'
)

# Find tournaments with the most participants
from django.db.models import Count
popular_tournaments = Tournament.objects.annotate(
    participant_count=Count('members')
).order_by('-participant_count')
```

## Quick Reference

Here's a concise summary of relationship types:

**ForeignKey (Many-to-One)**
- Rails: `belongs_to :team` and `has_many :members`
- Django: `team = models.ForeignKey(Team, related_name='members')`
- Direction: Define in the "child" model (where belongs_to would go)
- Access: `member.team` and `team.members.all()`

**OneToOneField (One-to-One)**
- Rails: `belongs_to :member` and `has_one :profile`
- Django: `member = models.OneToOneField(Member, related_name='profile')`
- Direction: Define in the dependent model (where belongs_to would go)
- Access: `profile.member` and `member.profile`

**ManyToManyField (Many-to-Many)**
- Rails: `has_many :through` on both sides
- Django: `tournaments = models.ManyToManyField(Tournament, related_name='members')`
- Direction: Define in either model (your choice)
- Access: `member.tournaments.all()` and `tournament.members.all()`

**Key Parameters**
- `on_delete`: Required for ForeignKey/OneToOne; controls deletion behavior
- `related_name`: Name of the reverse relationship
- `null=True`: Allows NULL in database
- `blank=True`: Allows empty value in forms
- `through`: Specifies through model for ManyToMany with extra fields

## Common Pitfalls

**Forgetting on_delete**
```python
# ERROR: on_delete is required
team = models.ForeignKey(Team)

# CORRECT
team = models.ForeignKey(Team, on_delete=models.CASCADE)
```

**Confusing null and blank**
- `null=True`: Database can store NULL
- `blank=True`: Forms can submit empty value
- Usually you want both or neither

**Not using related_name**
```python
# Without related_name
team = models.ForeignKey(Team, on_delete=models.CASCADE)
# Access via: team.member_set.all() (awkward)

# With related_name
team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
# Access via: team.members.all() (natural)
```

**Trying to define relationships on both sides**
```python
# DON'T DO THIS - Django will raise an error
class Team(models.Model):
    members = models.ManyToManyField(Member)  # Wrong!

class Member(models.Model):
    teams = models.ManyToManyField(Team)  # Also wrong!

# DO THIS - define on one side only
class Member(models.Model):
    teams = models.ManyToManyField(Team, related_name='members')

class Team(models.Model):
    pass  # No field needed - Django creates team.members automatically
```

## Summary

Django's approach to relationships emphasizes efficiency and consistency. While it differs from Rails' symmetric declarations, it provides the same functionality with less code and fewer chances for error.

Remember:
- **ForeignKey** creates many-to-one relationships (define where `belongs_to` would go)
- **OneToOneField** creates one-to-one relationships (define in the dependent model)
- **ManyToManyField** creates many-to-many relationships (define in either model)
- The `related_name` parameter creates the reverse relationship automatically
- Use `select_related` and `prefetch_related` to optimize queries

Once you internalize the pattern of defining relationships on one side, Django relationships become intuitive and powerful. The framework handles the complexity of reverse relationships, leaving you free to focus on your application logic.

