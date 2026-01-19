"""
URL configuration for my_tennis_club project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/

IMPORTANT: URL Structure for Multiple Apps
-------------------------------------------
Each app should have its own URL prefix to avoid conflicts:

    path('members/', include('members.urls'))   # Members app URLs
    path('teams/', include('teams.urls'))       # Teams app URLs
    path('blog/', include('blog.urls'))         # Blog app URLs
    path('api/', include('api.urls'))           # API app URLs

Rails equivalent:
    namespace :members do
        resources :members
    end

    namespace :teams do
        resources :teams
    end

Why use prefixes?
- Avoids URL conflicts between apps
- Makes URLs more readable and organized
- Allows app reusability across projects
- Better for large projects with many apps
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),

    # Members app - all member URLs start with /members/
    # Example: /members/, /members/new/, /members/1/, etc.
    path('members/', include('members.urls')),

    # If you add more apps, include them here with prefixes:
    # path('teams/', include('teams.urls')),
    # path('blog/', include('blog.urls')),
    # path('api/v1/', include('api.urls')),
]
