from django.urls import path

from client import views
from client.apps import ClientConfig

app_name = ClientConfig.name

urlpatterns = [
    path('client_list/', views.ClientListView.as_view(), name='client_list'),
    path('client/<int:pk>/detail/', views.ClientDetailView.as_view(), name='client_detail'),
    path('client/create/', views.ClientCreateView.as_view(), name='client_create'),
    path('client/<int:pk>/update/', views.ClientUpdateView.as_view(), name='client_update'),
    path('client/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    ]
