from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from client.models import Client
from client.forms import ClientForm


class ClientListView(ListView):
    model = Client
    template_name = 'client/client_list.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'client/client_detail.html'


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'
    success_url = reverse_lazy('client:client_list')

    def form_valid(self, form):
        client = form.save()
        user = self.request.user
        client.owner = user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'
    success_url = reverse_lazy('client:client_list')

    def get_success_url(self):
        return reverse('client:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'client/cclient_confirm_delete.html'
    success_url = reverse_lazy('client:client_list')

