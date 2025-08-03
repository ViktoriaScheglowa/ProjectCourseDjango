from django import forms
from django.core.exceptions import ValidationError
from django.forms import BooleanField, ModelForm

from client.models import Client
from mailing.models import Mailing
from message.models import Message


# DICT = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class DateTimeLocalInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_custom_help_texts()
        self.apply_styling()
        self.clean_widget_attrs()

    def set_custom_help_texts(self):
        """Установление кастомных подсказок для полей"""
        password_help_texts = {
            'password1': 'Придумайте пароль, содержащий не менее 8 символов',
            'password2': 'Введите пароль еще раз'
        }
        for field_name, help_text in password_help_texts.items():
            if field_name in self.fields:
                self.fields[field_name].help_text = help_text

    def apply_styling(self):
        """Применение стилизации ко всем полям"""

        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'

            if field.help_text:
                field.widget.attrs['placeholder'] = field.help_text
                field.widget.attrs['data-help'] = field.help_text
                field.help_text = ''

            if isinstance(field, forms.Textarea):
                field.widget.attrs.update({
                    'rows': 8,
                    'class': 'form-control message-textarea'
                })
            elif isinstance(field, forms.DateTimeField):
                field.widget = DateTimeLocalInput()
                field.widget.attrs.update({
                    'class': 'form-control datetimepicker',
                    'autocomplete': 'off'
                })

    def clean_widget_attrs(self):
        """Очистка всех нежелательных атрибутов виджета"""
        attrs_to_remove = [
            'aria-describedby',
            'data-toggle',
            'data-placement',
            'title',
            'data-original-title'
        ]

        for field in self.fields.values():
            for attr in attrs_to_remove:
                field.widget.attrs.pop(attr, None)


class MailingUForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_sending', 'end_sending', 'status', 'client', 'message']


class MailingForm(StyleFormMixin, ModelForm):
    message = forms.ModelChoiceField(queryset=Message.objects.all())
    clients = forms.ModelMultipleChoiceField(
        queryset=Client.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Mailing
        fields = ['message', 'clients', 'start_sending', 'end_sending']


class MailingManagerForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Mailing
        fields = ['status']



    # def clean(self):
    #     cleaned_data = super().clean()
    #     name = cleaned_data.get("name")
    #     description = cleaned_data.get("description")
    #
    #     if name:
    #         self.validate_forbidden_words(name)
    #     if description:
    #         self.validate_forbidden_words(description)
    #
    #     return cleaned_data
    #
    # def validate_forbidden_words(self, value):
    #     for word in DICT:
    #         if word.lower() in value.lower():
    #             raise forms.ValidationError(f"Слово '{word}' запрещено использовать.")
    #
    # def clean_price(self):
    #     price = self.cleaned_data.get("price")
    #
    #     if price is not None and price <= 0:
    #         raise forms.ValidationError("Цена не может быть отрицательной.")
    #
    #     return price


# class MailingModeratorForm(StyleFormMixin, ModelForm):
#     class Meta:
#         model = Mailing
#         fields = "__all__"
