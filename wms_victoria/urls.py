"""
URL configuration for wms_victoria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from users.views import custom_logout
from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from myapp.views import MyModelViewSet


urlpatterns = [
    path('', lambda request: redirect('login', permanent=True)),  # Redirect root to login
    path('admin/logout/', custom_logout, name='admin_logout'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('inventory/', include('inventory.urls')),
    #path("__reload__/", include("django_browser_reload.urls")),
    
    
]
