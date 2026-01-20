# Django ORM and Database Queries

This section covers how to query data in Django, with comprehensive comparisons to Rails ActiveRecord.

## Documents in This Section

### [Django ORM vs Rails Active Record](DJANGO-ORM-VS-RAILS-ACTIVE-RECORD.md)
**Complete comparison** - Every query pattern side-by-side

**What's covered:**
- Complete comparison table (30+ operations)
- Field lookups (`__gt`, `__contains`, `__iexact`, etc.)
- Filtering and querying patterns
- Ordering and limiting results
- Aggregations (Count, Sum, Avg, Max, Min)
- Eager loading strategies
- Custom managers (Django's version of scopes)
- QuerySet lazy evaluation
- Raw SQL when needed

**Reading time:** 20-30 minutes

---

## Quick Reference

### Common Operations

| Task | Rails | Django |
|------|-------|--------|
| **Get all** | `User.all` | `User.objects.all()` |
| **Filter** | `User.where(active: true)` | `User.objects.filter(active=True)` |
| **Get one** | `User.find_by(email: '...')` | `User.objects.get(email='...')` |
| **Order** | `User.order(created_at: :desc)` | `User.objects.order_by('-created_at')` |
| **Limit** | `User.limit(10)` | `User.objects.all()[:10]` |
| **Count** | `User.count` | `User.objects.count()` |
| **Create** | `User.create(name: 'John')` | `User.objects.create(name='John')` |
| **Eager load** | `User.includes(:posts)` | `User.objects.prefetch_related('posts')` |

### Key Differences

1. **Manager access:** Django uses `Model.objects.method()` instead of `Model.method`
2. **Field lookups:** Django uses double underscores: `age__gt=18`, `name__icontains='john'`
3. **Ordering:** Use minus sign for descending: `order_by('-created_at')`
4. **Slicing:** Python slicing `[:10]` instead of `.limit(10)`
5. **Lazy evaluation:** Django QuerySets don't execute until you iterate

### Field Lookups

Django's powerful double-underscore syntax:

```python
# Greater than
User.objects.filter(age__gt=18)

# Case-insensitive contains
User.objects.filter(name__icontains='john')

# Starts with
User.objects.filter(email__startswith='admin@')

# In list
User.objects.filter(status__in=['active', 'pending'])

# Null check
User.objects.filter(deleted_at__isnull=True)

# Date parts
Post.objects.filter(created_at__year=2026)
```

---

## When to Use This Guide

- **Translating Rails queries:** Look up the Rails method, find the Django equivalent
- **Learning patterns:** Read through to understand Django's querying philosophy
- **Quick reference:** Bookmark this page for daily development
- **Performance tuning:** Learn about eager loading and optimization

---

## Next Steps

After learning ORM basics:
1. Explore [Model Relationships](../relationships/) for querying across relationships
2. Check [Advanced Topics](../advanced/) for complex queries and custom managers
3. Practice with the [Getting Started Guide](../getting-started/03-GETTING-STARTED.md)

---

[← Back to Documentation Home](../README.md)

