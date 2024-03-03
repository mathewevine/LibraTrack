"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from LibraTrack import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login_view),
    path('logout/', views.LogoutView.as_view()),
    path('addBook/', views.add_book),
    path('books/', views.get_all_books),
    #path('rentBook/', views.rent_book),
    path('users/', views.get_all_users),
    path('rentedBooks/', views.get_all_rented_books),
    path('csrf-token/', views.GetCSRFToken.as_view()),
    path('delete/', views.DeleteAccountView.as_view()),
    path('add-notification/', views.add_notification),
    path('favicon.ico', views.favicon_view),
    path('notifications/', views.get_all_notifications),
    path('reset-password/<str:register_no>/', views.reset_password),
    path('delete-user/<str:register_no>/', views.delete_user),
    path('update-user/<str:register_no>/', views.update_user),
    path('update-book/<str:book_id>/', views.update_book),
    path('delete-book/<str:book_id>/', views.delete_book),
]
