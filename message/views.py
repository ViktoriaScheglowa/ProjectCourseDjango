from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView

from message.forms import MessageForm
from message.models import Message


class MessageListView(ListView):
    model = Message
    template_name = 'message/message_list.html'


class MessageDetailView(DetailView):
    model = Message
    template_name = 'message/message_detail.html'


class MessageCreateView(CreateView):
    model = Message
    template_name = 'message/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'message/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')

    def get_success_url(self):
        return reverse('message:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'message/message_confirm_delete.html'
    success_url = reverse_lazy('message:message_list')

