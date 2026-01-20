# Advanced Django Topics

This section covers deeper Django concepts including models, forms, and the admin interface.

## Documents in This Section

### [Models, Forms & Admin](02-MODELS-FORMS-ADMIN.md)
**Deep dive** - Understanding Django's architecture

**What's covered:**
- **Models and Meta Class** - What is Meta? All options explained
- **Field types** - CharField, EmailField, DateField, and more
- **Forms and ModelForm** - Creating forms, widgets, validation
- **Admin Configuration** - list_display, fieldsets, search_fields, etc.
- **Visual diagrams** - How everything connects
- **Quick reference** - Line-by-line admin.py explanation
- **Rails comparisons** - For every concept

**Reading time:** 60-90 minutes

---

## What You'll Learn

### The Meta Class

Django's Meta class is unique—there's no direct Rails equivalent. It's used for model configuration:

```python
class Member(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['lastname', 'firstname']
        verbose_name = 'Member'
        verbose_name_plural = 'Members'
        db_table = 'members'
```

Common Meta options:
- `ordering` - Default sort order
- `verbose_name` - Human-readable name
- `db_table` - Custom table name
- `unique_together` - Compound unique constraints
- `indexes` - Database indexes

### Forms vs Rails Helpers

**Rails:**
```erb
<%= form_for @member do |f| %>
  <%= f.text_field :firstname %>
  <%= f.text_field :lastname %>
<% end %>
```

**Django:**
```python
# forms.py
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['firstname', 'lastname']

# template
{{ form.as_p }}
```

Django uses Form classes for more structure and reusability.

### Admin Interface

Django's admin is built-in and highly customizable:

```python
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['firstname', 'lastname', 'email', 'team']
    list_filter = ['team', 'joined_date']
    search_fields = ['firstname', 'lastname', 'email']
    ordering = ['lastname']
```

No gems needed—it's all part of Django!

---

## When to Read This

**Read this section when you:**
- Need to understand the Meta class
- Want to customize the admin interface
- Are building complex forms
- Need to know all field types available
- Want visual diagrams of how Django components connect

**Prerequisites:**
- Basic understanding of Django models
- Familiarity with the [Getting Started](../getting-started/) guide
- Knowledge of [Model Relationships](../relationships/)

---

## Quick Reference

### Common Field Types

| Rails | Django |
|-------|--------|
| `string` | `CharField(max_length=...)` |
| `text` | `TextField()` |
| `integer` | `IntegerField()` |
| `boolean` | `BooleanField()` |
| `datetime` | `DateTimeField()` |
| `date` | `DateField()` |
| `decimal` | `DecimalField(max_digits=..., decimal_places=...)` |

### Admin Customization

```python
@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    # What columns to show
    list_display = ['field1', 'field2', 'custom_method']
    
    # Filters in sidebar
    list_filter = ['status', 'created_at']
    
    # Search functionality
    search_fields = ['name', 'email']
    
    # Default ordering
    ordering = ['-created_at']
    
    # Organize form fields
    fieldsets = (
        ('Section 1', {'fields': ('field1', 'field2')}),
        ('Section 2', {'fields': ('field3', 'field4')}),
    )
```

---

## Next Steps

After mastering these concepts:
1. Build custom forms for your models
2. Customize the admin interface for your needs
3. Explore Django's validation system
4. Learn about custom field types
5. Study form widgets and customization

---

[← Back to Documentation Home](../README.md)

