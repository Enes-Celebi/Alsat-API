from django.urls import path
from app.views.auth_view import signup_view

urlpatterns = [
    path('api/auth/signup', signup_view, name='signup'),
]