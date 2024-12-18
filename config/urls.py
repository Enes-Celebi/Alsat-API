from django.urls import path
from app.views.auth_view import signup_view, signin_view

urlpatterns = [
    path('api/auth/signup', signup_view, name='signup'),
    path('api/auth/signin', signin_view, name='signin')
]