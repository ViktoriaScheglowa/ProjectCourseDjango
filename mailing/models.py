from django.db import models

from client.models import Client
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


class Mailing(models.Model):
    CREATED = 'Создана'
    ACTIVATED = 'Запущена'
    ENDED = 'Завершена'

    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (ACTIVATED, 'Запущена'),
        (ENDED, 'Завершена'),
    ]

    start_sending = models.DateTimeField(
        verbose_name='Начало рассылки',
        help_text='Введите дату и время начала рассылки'
    )
    end_sending = models.DateTimeField(
        verbose_name='Окончание рассылки',
        help_text='Введите дату и время окончания рассылки'
    )
    status = models.CharField(
        max_length=9,
        choices=STATUS_CHOICES,
        default=CREATED,
        verbose_name='Статус',
        help_text='Статус рассылки'
    )
    message = models.ForeignKey(
        to=Message,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Письмо'
    )
    client = models.ManyToManyField(
        to=Client,
        related_name='client',
        verbose_name='Получатели'
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Укажите владельца',
        related_name='mailing_owner',
        verbose_name='Автор'
    )

    def __str__(self):
        return (f'Статус рассылки: {self.status}\n'
                f'Период рассылки: {self.start_sending} - {self.end_sending}\n'
                f'Получатели: {self.client}\n'
                f'Сообщение: {self.message}')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        ordering = ['status', 'end_sending', 'start_sending',]


class MailingAttempt(models.Model):
    SUCCESS = 'Успешно'
    UNSUCCESS = 'Не успешно'

    STATUS_CHOICES = [
        (SUCCESS, 'Успешно'),
        (UNSUCCESS, 'Не успешно')
    ]

    date_attempt = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время попытки рассылки'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=UNSUCCESS,
        verbose_name='Статус',
        help_text='Статус попытки рассылки'
    )
    answer = models.TextField(
        verbose_name='Ответ почтового сервера'
    )
    mailing = models.ForeignKey(
        Mailing,
        on_delete=models.CASCADE,
        related_name='attempts',
        null=True,
        blank=True,
        verbose_name='Рассылка'
    )

    def __str__(self):
        return (f'Статус: {self.status},'
                f'Тема письма: {self.mailing.message.subject}'
                f'Дата попытки: {self.date_attempt},'
                f'Ответ сервера: {self.answer}')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылок'
        ordering = ['status', 'date_attempt',]
