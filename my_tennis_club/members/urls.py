from django.urls import path
from . import views

"""
URL Configuration for Members app
Rails equivalent: resources :members
"""

urlpatterns = [
    # ========== HTML VIEWS (CRUD) ==========
    # INDEX - List all members
    path('', views.member_list, name='member_list'),

    # NEW/CREATE - Show form and create member
    path('new/', views.member_create, name='member_create'),

    # SHOW - Display single member (must come after 'new/')
    path('<int:pk>/', views.member_detail, name='member_detail'),

    # EDIT/UPDATE - Show form and update member
    path('<int:pk>/edit/', views.member_update, name='member_update'),

    # DELETE - Delete member
    path('<int:pk>/delete/', views.member_delete, name='member_delete'),


    # ========== AJAX/JSON API ENDPOINTS ==========
    # API: List all members as JSON
    path('api/members/', views.member_list_json, name='member_list_json'),

    # API: Create member via AJAX
    path('api/members/create/', views.member_create_json, name='member_create_json'),

    # API: Get single member as JSON
    path('api/members/<int:pk>/', views.member_detail_json, name='member_detail_json'),

    # API: Update member via AJAX
    path('api/members/<int:pk>/update/', views.member_update_json, name='member_update_json'),

    # API: Delete member via AJAX
    path('api/members/<int:pk>/delete/', views.member_delete_json, name='member_delete_json'),
]

"""
Django URL patterns explained:
- path('', view) -> matches /members/
- path('new/', view) -> matches /members/new/
- path('<int:pk>/', view) -> matches /members/1/, /members/2/, etc.
- path('<int:pk>/edit/', view) -> matches /members/1/edit/

Rails equivalent:
resources :members do
  # creates: index, new, create, show, edit, update, destroy
end

Django requires explicit URL definitions (no magic routing)
"""

