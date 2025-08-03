from django.forms import ModelForm

from client.models import Client
from mailing.forms import StyleFormMixin


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)
