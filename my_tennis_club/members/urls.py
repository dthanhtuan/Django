from django.urls import path
from . import views

"""
URL Configuration for Members app

These URLs are RELATIVE to the prefix defined in the project urls.py.
Project urls.py has: path('members/', include('members.urls'))

So these URLs become:
- '' → /members/
- 'new/' → /members/new/
- '<int:pk>/' → /members/1/

Rails equivalent: resources :members
"""

# App namespace - allows {% url 'members:list' %} in templates
app_name = 'members'

urlpatterns = [
    # ========== HTML VIEWS (CRUD) ==========
    # INDEX - List all members
    # URL: /members/
    path('', views.member_list, name='list'),

    # NEW/CREATE - Show form and create member
    # URL: /members/new/
    path('new/', views.member_create, name='create'),

    # SHOW - Display single member (must come after 'new/')
    # URL: /members/1/
    path('<int:pk>/', views.member_detail, name='detail'),

    # EDIT/UPDATE - Show form and update member
    # URL: /members/1/edit/
    path('<int:pk>/edit/', views.member_update, name='update'),

    # DELETE - Delete member
    # URL: /members/1/delete/
    path('<int:pk>/delete/', views.member_delete, name='delete'),


    # ========== AJAX/JSON API ENDPOINTS ==========
    # API: List all members as JSON
    # URL: /members/api/members/
    path('api/members/', views.member_list_json, name='api_list'),

    # API: Create member via AJAX
    # URL: /members/api/members/create/
    path('api/members/create/', views.member_create_json, name='api_create'),

    # API: Get single member as JSON
    # URL: /members/api/members/1/
    path('api/members/<int:pk>/', views.member_detail_json, name='api_detail'),

    # API: Update member via AJAX
    # URL: /members/api/members/1/update/
    path('api/members/<int:pk>/update/', views.member_update_json, name='api_update'),

    # API: Delete member via AJAX
    # URL: /members/api/members/1/delete/
    path('api/members/<int:pk>/delete/', views.member_delete_json, name='api_delete'),
]

"""
Usage in templates (with namespace):
    {% url 'members:list' %}           → /members/
    {% url 'members:create' %}         → /members/new/
    {% url 'members:detail' pk=1 %}    → /members/1/
    {% url 'members:update' pk=1 %}    → /members/1/edit/

Usage in views (with namespace):
    from django.urls import reverse
    url = reverse('members:list')      → /members/
    url = reverse('members:detail', kwargs={'pk': 1})  → /members/1/

If you add more apps (teams, blog, etc.), they can have the same URL names:
    {% url 'members:list' %}  → /members/
    {% url 'teams:list' %}    → /teams/
    {% url 'blog:list' %}     → /blog/

Rails comparison:
    resources :members do
      # creates: index, new, create, show, edit, update, destroy
    end
    
Django requires explicit URL definitions (no magic routing).
"""



