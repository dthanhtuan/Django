# Django ORM vs Rails Active Record: A Complete Comparison

If you're coming from Rails, Django's ORM will feel familiar in many ways—but there are important differences in how you query and manipulate data. This guide provides a comprehensive comparison to help you translate your Rails knowledge to Django.

## The Basics

In Rails, you work directly with model classes using Active Record methods. Django works similarly, but uses a "Manager" as an intermediary. By default, every Django model has a manager called `objects`:

**Rails:**
```ruby
User.all
User.find(1)
User.where(active: true)
```

**Django:**
```python
User.objects.all()
User.objects.get(id=1)
User.objects.filter(active=True)
```

The `objects` manager is Django's gateway to database operations. You can think of it as Rails' model class methods, just accessed through `.objects` first.

## Complete Comparison Table

| Operation | Rails Active Record | Django ORM | Notes |
|-----------|-------------------|------------|-------|
| **All records** | `User.all` | `User.objects.all()` | Django returns QuerySet (lazy) |
| **Find by ID** | `User.find(1)` | `User.objects.get(id=1)` | Django raises `DoesNotExist` if not found |
| **Find by attribute** | `User.find_by(email: 'user@example.com')` | `User.objects.get(email='user@example.com')` | Use `get()` for single record |
| **Where clause** | `User.where(active: true)` | `User.objects.filter(active=True)` | Returns multiple records |
| **Where NOT** | `User.where.not(active: true)` | `User.objects.exclude(active=True)` | Opposite of filter |
| **First record** | `User.first` | `User.objects.first()` | Returns None if empty (not exception) |
| **Last record** | `User.last` | `User.objects.last()` | Requires ordering to be meaningful |
| **Order by** | `User.order(:created_at)` | `User.objects.order_by('created_at')` | Use `-created_at` for DESC |
| **Order descending** | `User.order(created_at: :desc)` | `User.objects.order_by('-created_at')` | Note the minus sign |
| **Limit** | `User.limit(10)` | `User.objects.all()[:10]` | Django uses slicing |
| **Offset** | `User.offset(20)` | `User.objects.all()[20:30]` | Slice notation |
| **Count** | `User.count` | `User.objects.count()` | Both execute SQL COUNT |
| **Exists** | `User.exists?` | `User.objects.exists()` | Check if any records exist |
| **Distinct** | `User.distinct` | `User.objects.distinct()` | Remove duplicates |
| **Select specific fields** | `User.select(:id, :name)` | `User.objects.values('id', 'name')` | Returns dicts, not model instances |
| **Select (keep instances)** | `User.select(:id, :name)` | `User.objects.only('id', 'name')` | Returns model instances |
| **Pluck** | `User.pluck(:email)` | `User.objects.values_list('email', flat=True)` | Returns list of values |
| **Create** | `User.create(name: 'John')` | `User.objects.create(name='John')` | Creates and saves |
| **Build (new)** | `User.new(name: 'John')` | `User(name='John')` | Creates but doesn't save |
| **Update all** | `User.update_all(active: false)` | `User.objects.update(active=False)` | Bulk update |
| **Update single** | `user.update(name: 'Jane')` | `User.objects.filter(id=user.id).update(name='Jane')` | Or use instance method |
| **Delete all** | `User.destroy_all` | `User.objects.all().delete()` | Bulk delete |
| **Delete single** | `user.destroy` | `user.delete()` | Instance method |
| **Find or create** | `User.find_or_create_by(email: 'user@example.com')` | `User.objects.get_or_create(email='user@example.com')` | Returns tuple (object, created) |
| **Find or initialize** | `User.find_or_initialize_by(email: 'user@example.com')` | `User.objects.get_or_create(email='user@example.com', defaults={...})[0]` | More verbose in Django |

## Querying in Detail

### Simple Queries

**Finding a single record:**

Rails:
```ruby
# Find by ID
user = User.find(1)

# Find by attribute (returns nil if not found)
user = User.find_by(email: 'john@example.com')

# Find by attribute (raises exception if not found)
user = User.find_by!(email: 'john@example.com')
```

Django:
```python
# Find by ID
user = User.objects.get(id=1)  # Raises DoesNotExist if not found

# Find by attribute
try:
    user = User.objects.get(email='john@example.com')
except User.DoesNotExist:
    user = None

# Or use filter().first() to get None instead of exception
user = User.objects.filter(email='john@example.com').first()
```

**Finding multiple records:**

Rails:
```ruby
# All users
users = User.all

# Where clause
active_users = User.where(active: true)

# Multiple conditions
users = User.where(active: true, role: 'admin')

# Chaining
users = User.where(active: true).where(role: 'admin')
```

Django:
```python
# All users
users = User.objects.all()

# Filter clause
active_users = User.objects.filter(active=True)

# Multiple conditions (AND)
users = User.objects.filter(active=True, role='admin')

# Chaining
users = User.objects.filter(active=True).filter(role='admin')

# OR conditions
from django.db.models import Q
users = User.objects.filter(Q(role='admin') | Q(role='moderator'))
```

### Field Lookups

Django provides powerful field lookups that go beyond simple equality:

Rails:
```ruby
# Greater than
User.where('age > ?', 18)

# LIKE query
User.where('name LIKE ?', 'John%')

# IN query
User.where(status: ['active', 'pending'])

# Case insensitive
User.where('LOWER(email) = ?', 'john@example.com'.downcase)
```

Django:
```python
# Greater than
User.objects.filter(age__gt=18)

# Greater than or equal
User.objects.filter(age__gte=18)

# Less than
User.objects.filter(age__lt=65)

# LIKE query (case-sensitive)
User.objects.filter(name__startswith='John')

# ILIKE query (case-insensitive)
User.objects.filter(name__istartswith='john')

# Contains
User.objects.filter(name__contains='oh')

# IN query
User.objects.filter(status__in=['active', 'pending'])

# Case insensitive exact match
User.objects.filter(email__iexact='john@example.com')

# Null checks
User.objects.filter(deleted_at__isnull=True)
```

Common Django lookup suffixes:
- `__exact` - Exact match (default)
- `__iexact` - Case-insensitive exact match
- `__contains` - Contains substring
- `__icontains` - Case-insensitive contains
- `__gt`, `__gte` - Greater than, greater than or equal
- `__lt`, `__lte` - Less than, less than or equal
- `__in` - In a list
- `__startswith`, `__istartswith` - Starts with
- `__endswith`, `__iendswith` - Ends with
- `__isnull` - Is null check
- `__range` - Between two values

### Ordering and Limiting

Rails:
```ruby
# Order by one field
User.order(:created_at)

# Order descending
User.order(created_at: :desc)

# Multiple orderings
User.order(:role, created_at: :desc)

# Limit
User.limit(10)

# Offset and limit
User.offset(20).limit(10)

# First and last
User.first
User.last
```

Django:
```python
# Order by one field
User.objects.order_by('created_at')

# Order descending (note the minus!)
User.objects.order_by('-created_at')

# Multiple orderings
User.objects.order_by('role', '-created_at')

# Limit (using slicing)
User.objects.all()[:10]

# Offset and limit
User.objects.all()[20:30]

# First and last
User.objects.first()  # Returns None if empty
User.objects.last()   # Requires ordering
```

### Aggregations and Annotations

Rails:
```ruby
# Count
User.count
User.where(active: true).count

# Sum
Order.sum(:total)

# Average
Product.average(:price)

# Maximum
Product.maximum(:price)

# Minimum
Product.minimum(:price)

# Group and count
User.group(:role).count
```

Django:
```python
from django.db.models import Count, Sum, Avg, Max, Min

# Count
User.objects.count()
User.objects.filter(active=True).count()

# Sum
Order.objects.aggregate(Sum('total'))

# Average
Product.objects.aggregate(Avg('price'))

# Maximum
Product.objects.aggregate(Max('price'))

# Minimum
Product.objects.aggregate(Min('price'))

# Group and count
User.objects.values('role').annotate(count=Count('id'))

# Annotate each object with related count
User.objects.annotate(order_count=Count('orders'))
```

## Relationships and Joins

### Accessing Related Objects

Rails:
```ruby
# Has many
user.posts.all
user.posts.where(published: true)

# Belongs to
post.author

# Has one
user.profile
```

Django:
```python
# Has many (reverse ForeignKey)
user.posts.all()
user.posts.filter(published=True)

# Belongs to (ForeignKey)
post.author

# Has one (reverse OneToOneField)
user.profile
```

### Eager Loading

Rails:
```ruby
# Includes (eager load)
users = User.includes(:posts)

# Multiple associations
users = User.includes(:posts, :profile)

# Nested includes
users = User.includes(posts: :comments)

# Joins (for filtering)
users = User.joins(:posts).where(posts: { published: true })
```

Django:
```python
# Select related (for ForeignKey, OneToOne)
users = User.objects.select_related('profile')

# Prefetch related (for reverse ForeignKey, ManyToMany)
users = User.objects.prefetch_related('posts')

# Multiple relations
users = User.objects.select_related('profile').prefetch_related('posts')

# Nested prefetch
from django.db.models import Prefetch
users = User.objects.prefetch_related(
    Prefetch('posts', queryset=Post.objects.select_related('category'))
)

# Joins (for filtering)
users = User.objects.filter(posts__published=True)
```

### Spanning Relationships

Rails:
```ruby
# Filter by related model
posts = Post.where(author: { active: true }).joins(:author)

# Access related fields
Post.joins(:author).where('users.active = ?', true)
```

Django:
```python
# Filter by related model (double underscore!)
posts = Post.objects.filter(author__active=True)

# Chain through multiple relationships
comments = Comment.objects.filter(post__author__active=True)

# Access related fields in ordering
posts = Post.objects.order_by('author__name')
```

## Creating and Updating Records

### Creating Records

Rails:
```ruby
# Create and save
user = User.create(name: 'John', email: 'john@example.com')

# Build (new) without saving
user = User.new(name: 'John')
user.save

# Create multiple
User.create([
  { name: 'John', email: 'john@example.com' },
  { name: 'Jane', email: 'jane@example.com' }
])
```

Django:
```python
# Create and save
user = User.objects.create(name='John', email='john@example.com')

# Build without saving
user = User(name='John')
user.save()

# Bulk create (more efficient)
User.objects.bulk_create([
    User(name='John', email='john@example.com'),
    User(name='Jane', email='jane@example.com')
])
```

### Updating Records

Rails:
```ruby
# Update instance
user.update(name: 'Jane')

# Update attributes without validation
user.update_attribute(:name, 'Jane')

# Update all matching records
User.where(active: false).update_all(status: 'inactive')

# Update or create
user = User.find_or_initialize_by(email: 'john@example.com')
user.update(name: 'John')
```

Django:
```python
# Update instance
user.name = 'Jane'
user.save()

# Update with method (saves immediately)
User.objects.filter(id=user.id).update(name='Jane')

# Update all matching records
User.objects.filter(active=False).update(status='inactive')

# Update specific fields only
user.save(update_fields=['name'])

# Get or create
user, created = User.objects.get_or_create(
    email='john@example.com',
    defaults={'name': 'John'}
)

# Update or create
user, created = User.objects.update_or_create(
    email='john@example.com',
    defaults={'name': 'John', 'active': True}
)
```

## Deleting Records

Rails:
```ruby
# Delete instance
user.destroy

# Delete without callbacks
user.delete

# Delete all matching
User.where(active: false).destroy_all

# Delete all (faster, no callbacks)
User.where(active: false).delete_all
```

Django:
```python
# Delete instance
user.delete()

# Delete all matching
User.objects.filter(active=False).delete()

# Delete all
User.objects.all().delete()
```

Note: Django doesn't distinguish between `delete` and `destroy` like Rails does. The `delete()` method always triggers signals (Django's equivalent of callbacks).

## Custom Managers

Rails:
```ruby
class User < ApplicationRecord
  scope :active, -> { where(active: true) }
  scope :recent, -> { where('created_at > ?', 1.week.ago) }
  
  def self.admins
    where(role: 'admin')
  end
end

# Usage
User.active
User.recent
User.admins
```

Django:
```python
class UserManager(models.Manager):
    def active(self):
        return self.filter(active=True)
    
    def recent(self):
        from datetime import timedelta
        from django.utils import timezone
        week_ago = timezone.now() - timedelta(days=7)
        return self.filter(created_at__gt=week_ago)
    
    def admins(self):
        return self.filter(role='admin')

class User(models.Model):
    # Fields...
    
    objects = UserManager()

# Usage
User.objects.active()
User.objects.recent()
User.objects.admins()

# Chaining works
User.objects.active().recent()
```

## QuerySet vs Array

A key difference: Rails' Active Record returns Arrays, while Django returns QuerySets (which are lazy).

Rails:
```ruby
users = User.where(active: true)  # Executes SQL immediately
users.class  # => Array (in Rails 5+) or ActiveRecord::Relation

# Iterating executes if not already executed
users.each { |u| puts u.name }
```

Django:
```python
users = User.objects.filter(active=True)  # Does NOT execute SQL yet
type(users)  # => QuerySet

# SQL executes when you:
# - Iterate
for user in users:
    print(user.name)

# - Convert to list
user_list = list(users)

# - Count
count = users.count()

# - Index/slice
first_user = users[0]

# - Evaluate as boolean
if users:
    print("Has users")
```

This laziness allows efficient chaining:

```python
# Only one SQL query for all this:
users = User.objects.filter(active=True)\
                    .filter(role='admin')\
                    .order_by('-created_at')[:10]
# SQL executes here when you iterate:
for user in users:
    print(user.name)
```

## Raw SQL

Sometimes you need raw SQL:

Rails:
```ruby
# Raw SQL
users = User.find_by_sql("SELECT * FROM users WHERE name LIKE 'J%'")

# Execute SQL
ActiveRecord::Base.connection.execute("UPDATE users SET active = true")
```

Django:
```python
# Raw SQL
users = User.objects.raw("SELECT * FROM users WHERE name LIKE 'J%'")

# Execute SQL
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute("UPDATE users SET active = true")
```

## Quick Reference Summary

**Most Common Operations:**

| Task | Rails | Django |
|------|-------|--------|
| Get all | `Model.all` | `Model.objects.all()` |
| Filter | `Model.where(field: value)` | `Model.objects.filter(field=value)` |
| Get one | `Model.find_by(field: value)` | `Model.objects.get(field=value)` |
| Create | `Model.create(attrs)` | `Model.objects.create(attrs)` |
| Update all | `Model.where(...).update_all(attrs)` | `Model.objects.filter(...).update(attrs)` |
| Delete all | `Model.where(...).destroy_all` | `Model.objects.filter(...).delete()` |
| Order | `Model.order(field: :desc)` | `Model.objects.order_by('-field')` |
| Limit | `Model.limit(10)` | `Model.objects.all()[:10]` |
| Count | `Model.count` | `Model.objects.count()` |
| Eager load | `Model.includes(:relation)` | `Model.objects.select_related('relation')` |

**Key Differences to Remember:**

1. **Manager access**: Django uses `Model.objects.method()`, Rails uses `Model.method`
2. **Lookups**: Django uses `field__lookup` (double underscore), Rails uses SQL or Arel
3. **Ordering**: Django uses `-field` for DESC, Rails uses `field: :desc`
4. **Slicing**: Django uses `[:10]`, Rails uses `.limit(10)`
5. **Lazy evaluation**: Django QuerySets are lazy, Rails often evaluates immediately
6. **Exceptions**: Django `get()` raises exceptions, Rails `find_by` returns nil

The good news? Once you understand these patterns, Django's ORM is just as powerful and intuitive as Rails' Active Record.

