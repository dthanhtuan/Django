# Model Relationships in Django

This section covers everything about model relationships in Django, with detailed comparisons to Rails ActiveRecord associations.

## Documents in This Section

### [Django vs Rails Relationships](DJANGO-VS-RAILS-RELATIONSHIPS.md) 🚨 **READ THIS FIRST**
**The critical difference** - Understanding one-side definitions

**What's covered:**
- The #1 thing that confuses Rails developers
- Why relationships are defined on ONE side only in Django
- How Django creates reverse relationships automatically
- Decision guide: which side to define the relationship on
- Mental models and practical examples

**Reading time:** 5-10 minutes

**⚠️ Important:** This explains the fundamental difference between Rails and Django relationships. Read this before anything else in this section!

---

### [Relationships Guide](RELATIONSHIPS-GUIDE.md)
**Complete reference** - All relationship types in detail

**What's covered:**
- **ForeignKey** (belongs_to) - Many-to-One relationships
- **OneToOneField** (has_one) - One-to-One relationships
- **Reverse relationships** (has_many) - One-to-Many relationships
- **ManyToManyField** (has_many :through) - Many-to-Many relationships
- Querying across relationships
- Performance optimization (select_related, prefetch_related)
- Practical examples from the tennis club app

**Reading time:** 30-45 minutes

---

### [Multiple ForeignKeys to Same Model](MULTIPLE-FOREIGNKEYS-SAME-MODEL.md)
**Important pattern** - Handling multiple relationships to the same model

**What's covered:**
- Why unique `related_name` is required
- Real-world examples (Match, Message, Team hierarchy)
- Self-referential ForeignKeys
- Naming conventions and best practices
- When to use `related_name='+'`
- Rails comparison

**Reading time:** 10-15 minutes

---

## Recommended Reading Order

1. **Essential:** [Django vs Rails Relationships](DJANGO-VS-RAILS-RELATIONSHIPS.md)
   - Understand the core difference first (5 minutes)
   - This prevents hours of confusion later

2. **Complete guide:** [Relationships Guide](RELATIONSHIPS-GUIDE.md)
   - Learn all relationship types in detail
   - See working examples from the project

3. **Special cases:** [Multiple ForeignKeys to Same Model](MULTIPLE-FOREIGNKEYS-SAME-MODEL.md)
   - When you need multiple ForeignKeys pointing to the same model
   - Important pattern to know

---

## Quick Reference

### Relationship Types

| Rails | Django | Define Where? |
|-------|--------|---------------|
| `belongs_to :team` | `ForeignKey(Team)` | In child model |
| `has_one :profile` | `OneToOneField` reverse | In dependent model |
| `has_many :members` | Reverse ForeignKey | Automatic via `related_name` |
| `has_many :through` | `ManyToManyField` | In either model |

### Key Difference

**Rails:** Define on both sides
```ruby
class Member < ApplicationRecord
  belongs_to :team
end

class Team < ApplicationRecord
  has_many :members
end
```

**Django:** Define on one side only
```python
class Member(models.Model):
    team = models.ForeignKey(Team, related_name='members')

class Team(models.Model):
    pass  # Django creates team.members automatically!
```

---

## Common Questions

**Q: Where do I define the relationship?**  
A: Where you would put `belongs_to` in Rails. See [Django vs Rails Relationships](DJANGO-VS-RAILS-RELATIONSHIPS.md).

**Q: What if I need multiple ForeignKeys to the same model?**  
A: Each needs a unique `related_name`. See [Multiple ForeignKeys to Same Model](MULTIPLE-FOREIGNKEYS-SAME-MODEL.md).

**Q: How do I query across relationships?**  
A: Use double underscores. See [Relationships Guide](RELATIONSHIPS-GUIDE.md) → Querying section.

---

[← Back to Documentation Home](../README.md)

