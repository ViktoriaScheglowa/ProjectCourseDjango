from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, ListView, DetailView, CreateView, UpdateView

from message.forms import MessageForm
from message.models import Message


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'message/message_list.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Message.objects.all()
        else:
            return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = 'message/message_detail.html'


class MessageCreateView(LoginRequiredMixin, CreateView):
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


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    template_name = 'message/message_form.html'
    form_class = MessageForm
    success_url = reverse_lazy('message:message_list')

    def get_success_url(self):
        return reverse('message:message_detail', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = 'message/message_confirm_delete.html'
    success_url = reverse_lazy('message:message_list')

