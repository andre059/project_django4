from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from users.forms import UserProfileForm, UserRegisterForm
from users.models import User
from .token import account_activation_token


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def __init__(self, **kwargs):
        super().__init__()
        self.method = None

    def form_valid(self, form):

        # Получаем пользователя из формы и делаем его не активным
        user = form.save()
        user.is_active = False
        user.save()

        # Отправляем письмо со ссылкой активации пользователя
        current_site = get_current_site(self.request)
        mail_subject = 'Ссылка для активации пользователя'
        message = render_to_string('users/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

        return super().form_valid(form)


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  # устанавливаем поле is_active в значение True
        user.save()  # сохраняем изменения в базе данных
        return render(request, 'users/success_verify.html')
    else:
        return render(request, 'users/invalid_link.html')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
