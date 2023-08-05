from django.urls import path
from .views import chat

urlpatterns = [
    path('v1/chat', chat, name='chat'),
]