from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from client.models import Client
from client.forms import ClientForm


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'client/client_list.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Client.objects.all()
        else:
            return Client.objects.filter(owner=self.request.user)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client
    template_name = 'client/client_detail.html'


class ClientCreateView(LoginRequiredMixin, CreateView):
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


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'
    success_url = reverse_lazy('client:client_list')

    def get_success_url(self):
        return reverse('client:client_detail', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    template_name = 'client/client_confirm_delete.html'
    success_url = reverse_lazy('client:client_list')

