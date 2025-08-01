from django.urls import path

from client import views
from client.apps import ClientConfig

app_name = ClientConfig.name

urlpatterns = [
    path('recipient_list/', views.ClientListView.as_view(), name='recipient_list'),
    path('recipient/<int:pk>/detail/', views.ClientDetailView.as_view(), name='recipient_detail'),
    path('recipient/create/', views.ClientCreateView.as_view(), name='recipient_create'),
    path('recipient/<int:pk>/update/', views.ClientUpdateView.as_view(), name='recipient_update'),
    path('recipient/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='recipient_delete'),
    ]
