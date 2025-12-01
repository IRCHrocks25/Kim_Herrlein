from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from myApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', include('dashboard.urls')),
    path('preview/home/', views.home_preview, name='home_preview'),
    path('', views.home, name='home'),
]