from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from client.models import Client
from mailing.forms import MailingForm, MailingManagerForm
from mailing.models import Mailing, MailingAttempt
from .services import send_message


def home(request):
    context = cache.get('home')

    if not context:
        total_mailings = Mailing.objects.count()
        active_mailings = Mailing.objects.filter(status='Запущена').count()

        # Получаем количество уникальных email-адресов получателей
        unique_clients = Client.objects.values('email').distinct().count()

        context = {
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'unique_clients': unique_clients,
        }
        cache.set('home', context, 60 * 15)

    return render(request, 'mailing/home.html', context)


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return Mailing.objects.all()
        else:
            return Mailing.objects.filter(owner=self.request.user)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            queryset = cache.get('mailing_list_for_manager')
            if not queryset:
                queryset = super().get_queryset()
                cache.set('mailing_list_for_manager', queryset, 60 * 15)  # Кешируем данные на 15 минут
            return queryset
        return super().get_queryset()


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

    def get_success_url(self):
        return reverse('mailing:mailing_detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingForm
        elif user.groups.filter(name='Manager').exists():
            return MailingManagerForm
        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt_list.html'
    context_object_name = 'attempts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attempts = self.get_queryset()
        context['total_attempts'] = attempts.count()
        context['successful_attempts'] = attempts.filter(status='Успешно').count()
        context['unsucessful_attempts'] = attempts.filter(status='Не успешно').count()
        context['sending_mails'] = sum(
            attempt.mailing.client.count()
            for attempt in attempts.filter(status='Успешно')
        )
        return context

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("Вы не авторизованы")

        cache_key = f'mailing_attempts_user_{self.request.user.pk}'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = MailingAttempt.objects.filter(mailing__owner=self.request.user).order_by('-date_attempt')
            cache.set(cache_key, queryset, 60 * 15)

        return queryset


class MailingAttemptDetailView(LoginRequiredMixin, DetailView):
    model = MailingAttempt
    template_name = 'mailing/mailing_attempt_detail.html'


class SendMailingView(View):
    template_name = 'mailing/send_mailing.html'

    def get(self, request, pk):
        mailing = get_object_or_404(Mailing, pk=pk, owner=request.user)

        success = send_message(mailing.pk, request)

        if success:
            print('Рассылка успешно отправлена')
        else:
            print('Рассылка не отправлена')

        return redirect('mailing:mailing_list')

