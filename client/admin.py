from django.contrib import admin

from client.models import Client


@admin.register(Client)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'message')
    list_filter = ('full_name', 'email')
    search_fields = ('full_name',)