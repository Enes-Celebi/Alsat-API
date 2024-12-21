from django.urls import path
from app.views.auth_view import signup_view, signin_view
from app.views.item_view import post_item, get_items, get_user_items, user_items_view
from app.views.chat_view import start_chat_view, get_chat_messages, send_message_view

urlpatterns = [
    path('api/auth/signup', signup_view, name='signup'),
    path('api/auth/signin', signin_view, name='signin'),

    path('api/item/post-item', post_item, name='post-item'),
    path('api/item/browse-items', get_items, name='get_items'),
    path('api/items/', user_items_view, name='get_own-items'),  
    path('api/items/<int:user_id>/', user_items_view, name='get_user_items'), 
    path('api/items/update/<int:item_id>/', user_items_view, name='update_item'),


    path('api/chat/start-chat/<int:item_id>/', start_chat_view, name='start-chat'),
    path('api/chat/<int:chat_id>/messages/', get_chat_messages, name='get-chat-messages'),
    path('api/chat/<int:chat_id>/send-message/', send_message_view, name='send-message'),
] 