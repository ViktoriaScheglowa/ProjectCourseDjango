from django.contrib import admin

from mailing.models import Mailing, MailingAttempt


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('start_sending', 'end_sending', 'status')
    list_filter = ('status', 'start_sending', 'end_sending')


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ('answer', 'status')
