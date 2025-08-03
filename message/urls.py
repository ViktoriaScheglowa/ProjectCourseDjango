from django.contrib import admin
from django.urls import path

from message import views
from message.apps import MessageConfig

app_name = MessageConfig.name

urlpatterns = [
    path('message_list/', views.MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/detail/', views.MessageDetailView.as_view(), name='message_detail'),
    path('message/create/', views.MessageCreateView.as_view(), name='message_create'),
    path('message/<int:pk>/update/', views.MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/', views.MessageDeleteView.as_view(), name='message_delete'),

    ]
