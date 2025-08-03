from django.forms import ModelForm

from mailing.forms import StyleFormMixin
from message.models import Message


class MessageForm(StyleFormMixin, ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for field in self._meta.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

    class Meta:
        model = Message
        fields = "subject", "text"
        exclude = ("owner",)
