from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('registration-successful/', views.registration_successful, name='registration_successful'),
    path('registration-pending/', views.registration_pending, name='registration_pending'),
    path('registration-failed/', views.registration_failed, name='registration_failed'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('warehouse_manager_dashboard/', views.warehouse_manager_dashboard, name='warehouse_manager_dashboard'),
    path('logout/', views.custom_logout, name='logout'),
    path('warehouse_staff_dashboard/', views.warehouse_staff_dashboard, name='warehouse_staff_dashboard'),
    path('unauthorized/', views.unauthorized_access, name='unauthorized'),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
    path('password_request_sent/', views.password_request_sent, name='password_request_sent'),
    path('admin/logout/', views.custom_logout, name='admin_logout'),
    
    

]
