from django.urls import path
from app.views.auth_view import signup_view, signin_view
from app.views.item_view import post_item, get_items

urlpatterns = [
    path('api/auth/signup', signup_view, name='signup'),
    path('api/auth/signin', signin_view, name='signin'),
    path('api/item/post-item', post_item, name='post-item'),
    path('api/item/browse-items', get_items, name='get_items'),
]