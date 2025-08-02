from django.contrib.auth.views import LoginView, LogoutView, PasswordResetCompleteView, PasswordResetConfirmView, \
    PasswordResetDoneView, PasswordResetView
from django.urls import path, reverse_lazy

from user.apps import UserConfig
from user.forms import CustomSetPasswordForm
from user.views import UserCreateView, email_verification, UserProfileUpdateView, block_user, UserListView

app_name = UserConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html"), name='login'),
    path("logout/", LogoutView.as_view(next_page=''), name='logout'),
    path("register/", UserCreateView.as_view(), name='register'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),
    path("email-confirm/<str:token>/", email_verification, name='email_confirm'),
    path('user_list/', UserListView.as_view(), name='user_list'),

    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset_form.html',
                                                      email_template_name='users/password_reset_email.html',
                                                      success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(form_class = CustomSetPasswordForm,
                                          template_name='users/password_reset_confirm.html',
                                          success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    path('user/<int:pk>/block/', block_user, name='block_user'),
]
