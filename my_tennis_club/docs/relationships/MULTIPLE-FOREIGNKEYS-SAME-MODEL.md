# Multiple ForeignKeys to the Same Model

When you have multiple foreign keys pointing to the same model, Django requires unique `related_name` values for each relationship. This is a common pattern that Rails developers need to understand when transitioning to Django.

## The Problem

In Rails, you might have a model with multiple associations to the same model:

```ruby
class Post < ApplicationRecord
  belongs_to :author, class_name: 'User'
  belongs_to :editor, class_name: 'User'
  belongs_to :reviewer, class_name: 'User'
end

class User < ApplicationRecord
  has_many :authored_posts, class_name: 'Post', foreign_key: 'author_id'
  has_many :edited_posts, class_name: 'Post', foreign_key: 'editor_id'
  has_many :reviewed_posts, class_name: 'Post', foreign_key: 'reviewer_id'
end
```

In Django, if you try to do this without unique `related_name` values, you'll get an error.

## The Django Solution

You must specify a unique `related_name` for each ForeignKey:

```python
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    
    # Multiple ForeignKeys to User - each needs unique related_name
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_posts'  # ← Unique related_name
    )
    
    editor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='edited_posts'  # ← Different from 'authored_posts'
    )
    
    reviewer = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_posts'  # ← Different from others
    )
```

## Why This Is Required

Django needs to know what to call the reverse relationship on the User model. Without unique names, there would be a conflict:

```python
# Without unique related_name, Django wouldn't know which posts to return
user.posts.all()  # Which posts? Authored? Edited? Reviewed?

# With unique related_name, it's clear:
user.authored_posts.all()   # Posts this user wrote
user.edited_posts.all()     # Posts this user edited
user.reviewed_posts.all()   # Posts this user reviewed
```

## What Happens If You Forget

If you try to create multiple ForeignKeys without unique `related_name` values:

```python
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    editor = models.ForeignKey(User, on_delete=models.CASCADE)  # ERROR!
```

Django will raise a `SystemCheckError`:

```
fields.E304: Reverse accessor for 'Post.author' clashes with reverse accessor for 'Post.editor'.
HINT: Add or change a related_name argument to the definition for 'Post.author' or 'Post.editor'.
```

## Real-World Examples

### Example 1: Message System

```python
class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    # Sender and recipient are both Users
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    
    # Now you can do:
    # user.sent_messages.all()
    # user.received_messages.all()
```

### Example 2: Team Hierarchy

```python
class Team(models.Model):
    name = models.CharField(max_length=255)
    
    # Self-referential ForeignKey (team can have parent team)
    parent_team = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subteams'  # Important for self-referential!
    )
    
    # Usage:
    # parent.subteams.all()  # Get all child teams
    # child.parent_team      # Get parent team
```

### Example 3: Match/Game System

```python
class Match(models.Model):
    date = models.DateField()
    location = models.CharField(max_length=255)
    
    # Two teams in a match
    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='home_matches'
    )
    
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='away_matches'
    )
    
    # Get winner (also a team)
    winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='won_matches'
    )
    
    # Now you can query:
    # team.home_matches.all()  # Matches where team is home
    # team.away_matches.all()  # Matches where team is away
    # team.won_matches.all()   # Matches team won
```

## Practical Usage

```python
# Create users
author = User.objects.create(username='alice')
editor = User.objects.create(username='bob')
reviewer = User.objects.create(username='charlie')

# Create post with multiple user relationships
post = Post.objects.create(
    title='My Article',
    content='Article content...',
    author=author,
    editor=editor,
    reviewer=reviewer
)

# Access from post (forward relationships)
print(post.author.username)    # 'alice'
print(post.editor.username)    # 'bob'
print(post.reviewer.username)  # 'charlie'

# Access from user (reverse relationships)
print(author.authored_posts.count())   # 1
print(editor.edited_posts.count())     # 1
print(reviewer.reviewed_posts.count()) # 1

# Query posts by different roles
alice_posts = Post.objects.filter(author=author)
bob_edits = Post.objects.filter(editor=editor)

# Get all posts a user is involved with (any role)
from django.db.models import Q
charlie_posts = Post.objects.filter(
    Q(author=reviewer) | Q(editor=reviewer) | Q(reviewer=reviewer)
)
```

## When You Don't Need Related Access

If you don't want reverse access from User to Posts, you can use `related_name='+'`:

```python
class AuditLog(models.Model):
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # User who performed action - no reverse access needed
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='+'  # Disables reverse relationship
    )
    
    # Now user.auditlog_set doesn't exist
    # You can only access: audit_log.user
```

This is useful for audit logs, history tables, or other cases where you don't need to query "all audit logs for this user" from the User model.

## Comparison with Rails

**Rails:**
```ruby
class Post < ApplicationRecord
  belongs_to :author, class_name: 'User'
  belongs_to :editor, class_name: 'User'
end

class User < ApplicationRecord
  has_many :authored_posts, class_name: 'Post', foreign_key: 'author_id'
  has_many :edited_posts, class_name: 'Post', foreign_key: 'editor_id'
end
```

**Django:**
```python
class Post(models.Model):
    author = models.ForeignKey(User, related_name='authored_posts')
    editor = models.ForeignKey(User, related_name='edited_posts')

class User(models.Model):
    # No need to define the reverse - Django creates it automatically
    pass
```

The key difference:
- **Rails**: You define both sides (`belongs_to` and `has_many`)
- **Django**: You define once with `related_name`, Django creates the reverse

## Common Naming Conventions

When naming related_name for multiple ForeignKeys to the same model:

**Pattern 1: Role-based**
```python
author = models.ForeignKey(User, related_name='authored_posts')
editor = models.ForeignKey(User, related_name='edited_posts')
reviewer = models.ForeignKey(User, related_name='reviewed_posts')
```

**Pattern 2: Action-based**
```python
sender = models.ForeignKey(User, related_name='sent_messages')
recipient = models.ForeignKey(User, related_name='received_messages')
```

**Pattern 3: Position-based**
```python
home_team = models.ForeignKey(Team, related_name='home_matches')
away_team = models.ForeignKey(Team, related_name='away_matches')
```

**Pattern 4: Descriptive**
```python
parent_team = models.ForeignKey('self', related_name='subteams')
manager = models.ForeignKey(User, related_name='managed_projects')
```

## Best Practices

1. **Always use descriptive related_name**
   ```python
   # Good
   author = models.ForeignKey(User, related_name='authored_posts')
   
   # Avoid - not clear what these posts are
   author = models.ForeignKey(User, related_name='posts1')
   ```

2. **Be consistent across your project**
   ```python
   # Consistent pattern: {role}_{model_plural}
   author = models.ForeignKey(User, related_name='authored_posts')
   owner = models.ForeignKey(User, related_name='owned_projects')
   creator = models.ForeignKey(User, related_name='created_tasks')
   ```

3. **Use plural for related_name (it returns a collection)**
   ```python
   # Good - plural
   related_name='authored_posts'
   
   # Avoid - singular
   related_name='authored_post'
   ```

4. **For self-referential ForeignKeys, always use related_name**
   ```python
   class Category(models.Model):
       name = models.CharField(max_length=255)
       parent = models.ForeignKey(
           'self',
           on_delete=models.CASCADE,
           null=True,
           related_name='children'  # Required!
       )
   ```

## Summary

**Key Points:**
- Multiple ForeignKeys to the same model **require** unique `related_name` values
- Django will raise an error if you forget
- Use descriptive names that explain the relationship
- Follow consistent naming patterns across your project
- You can use `related_name='+'` to disable reverse access if not needed

**Rails vs Django:**
- Rails: Define both `belongs_to` and `has_many` with `class_name` and `foreign_key`
- Django: Define once with unique `related_name`, Django creates reverse automatically

This is one of Django's requirements that actually makes code clearer—you're forced to think about and name each relationship explicitly!

