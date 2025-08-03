from django.contrib import admin
from django.urls import path

from mailing import views
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', views.home, name='home'),
    path('mailing_list/', views.MailingListView.as_view(), name='mailing_list'),
    path('mailing/<int:pk>/detail/', views.MailingDetailView.as_view(), name='mailing_detail'),
    path('mailing/create/', views.MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/update/', views.MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/<int:pk>/delete/', views.MailingDeleteView.as_view(), name='mailing_delete'),

    path('mailing_attempt_list/', views.MailingAttemptListView.as_view(), name='mailing_attempt_list'),
    path('mailing_attempt/<int:pk>/detail/', views.MailingAttemptDetailView.as_view(),
         name='mailing_attempt_detail'),
    path('mailing/<int:pk>/send/', views.SendMailingView.as_view(), name='send_mailing'),
]


