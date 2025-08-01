from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from client.models import Client
from .forms import ClientForm


class ClientListView(ListView):
    model = Client
    template_name = 'newsletters/recipient/recipient_list.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'newsletters/recipient/recipient_detail.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'newsletters/recipient/recipient_form.html'
    success_url = reverse_lazy('newsletters:recipient_list')

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'newsletters/recipient/recipient_form.html'
    success_url = reverse_lazy('newsletters:recipient_list')

    def get_success_url(self):
        return reverse('newsletters:recipient_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'newsletters/recipient/recipient_confirm_delete.html'
    success_url = reverse_lazy('newsletters:recipient_list')

