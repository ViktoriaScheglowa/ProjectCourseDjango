from django.db import models

from user.models import User


class Message(models.Model):
    subject = models.CharField(
        max_length=50,
        default='Без темы',
        null=True,
        blank=True,
        verbose_name='Тема письма',
        help_text='Введите тему письма'
    )
    text = models.TextField(
        verbose_name='Тело письма',
        help_text='Напишите письмо'
    )
    owner = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Укажите владельца',
        related_name='message_owner'
    )

    def __str__(self):
        return (f'Тема: {self.subject}\n'
                f'Сообщение: {self.text}')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['subject',]
