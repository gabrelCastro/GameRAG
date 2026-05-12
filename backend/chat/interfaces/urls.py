from django.urls import path

from chat.interfaces.views import ChatView

urlpatterns = [
    path('', ChatView.as_view(), name='chat'),
]
