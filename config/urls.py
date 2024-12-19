from django.urls import path
from app.views.auth_view import signup_view, signin_view
from app.views.item_view import post_item

urlpatterns = [
    path('api/auth/signup', signup_view, name='signup'),
    path('api/auth/signin', signin_view, name='signin'),
    path('api/item/post-item', post_item, name='post-item'),
]