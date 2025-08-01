import secrets

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from config.settings import EMAIL_HOST_USER
from user.forms import UserRegisterForm

from user.forms import UserProfileForm
from user.models import User


class UserCreateView(CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('mailing:mailing')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)

        user.token = token
        user.save()

        host = self.request.get_host()
        url = f"http://{host}/user/email-confirm/{token}"
        send_mail(
            subject="Добро пожаловать в наш сервис",
            message=f"Чтобы подтвердить почту, перейдите по ссылке {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("catalog:product_list"))


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'


def block_user(request, pk):
    if not request.user.has_perm('users.can_block_user'):
        messages.error(request, 'У вас нет прав для блокировки пользователей')
        return redirect('newsletters:home')

    user = get_object_or_404(User, pk=pk)
    user.is_active = False
    user.save()

    action = "разблокирован" if user.is_active else "заблокирован"
    return redirect('users:user_list')
