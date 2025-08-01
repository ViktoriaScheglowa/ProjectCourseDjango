from django.db import models

from user.models import User


class Client(models.Model):
    email = models.CharField(
        max_length=100,
        verbose_name='Электронная почта',
        help_text='Введите адрес электронной почты',
        unique=True
    )
    full_name = models.CharField(
        max_length=100,
        verbose_name='ФИО',
        help_text='Введите Ваше ФИО в именительном падеже'
    )
    message = models.TextField(
        verbose_name='Комментарий',
        help_text='Добавьте комментарий',
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        User,
        verbose_name='Владелец',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Укажите владельца',
        related_name='recipient_owner'
    )

    def __str__(self):
        return (f'ФИО: {self.full_name}\n'
                f'email: {self.email}\n'
                f'Комментарий: {self.message}')

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'
        ordering = ['full_name', 'email']

