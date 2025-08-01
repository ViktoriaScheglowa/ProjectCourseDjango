from django.contrib import admin

from mailing.models import Message, Mailing, MailingAttempt


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'text')
    list_filter = ('subject',)
    search_fields = ('text', 'subject')


@admin.register(Mailing)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('start_sending', 'end_sending', 'status')
    list_filter = ('status', 'start_sending', 'end_sending')


@admin.register(MailingAttempt)
class NewsletterAttemptAdmin(admin.ModelAdmin):
    list_display = ('answer', 'status')