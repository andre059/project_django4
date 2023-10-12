from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from django.http import HttpResponse

from django.contrib.sites.shortcuts import get_current_site
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail

from django.shortcuts import render, redirect

from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from django.conf import settings
from users.forms import UserProfileForm, UserRegisterForm
from users.models import User
from .token import account_activation_token
from .models import EmailVerificationToken


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def __init__(self, **kwargs):
        super().__init__()
        self.method = None

        # def form_valid(self, form):
        # Создаем пользователя, но пока не сохраняем
        # user = form.save(commit=False)
        # user.is_active = False  # Устанавливаем активность пользователя в False
        # user.save()  # Сохраняем пользователя

        # Генерируем и сохраняем токен подтверждения почты
        # token = get_random_string(length=32)
        # email_token = EmailVerificationToken.objects.create(user=user, token=token)

        # Отправляем письмо с токеном подтверждения
        # subject = 'Подтверждение почты'
        # message = f'Привет {user.username}, перейдите по ссылке для подтверждения вашей почты: ' \
        # f'{self.request.scheme}://{self.request.get_host()}/users/activate/{token}/'
        # from_email = settings.DEFAULT_FROM_EMAIL
        # recipient_list = [user.email]
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        # Сохраняем токен
        # email_token.save()

        # Перенаправляем пользователя на другую страницу после регистрации
        # return super().form_valid(form)

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


def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # сохранить форму в памяти, а не в базе данных
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Сгенерировать и сохранить токен подтверждения электронной почты
            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            email_token = EmailVerificationToken.objects.create(user=user, token=token, uid=uid)

            # Отправить электронное письмо с подтверждением
            current_site = get_current_site(request)
            mail_subject = 'Ссылка для активации была отправлена на ваш электронный адрес'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uidb64': uid,
                'token': token,
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()

            return HttpResponse('Пожалуйста, подтвердите свой адрес электронной почты, чтобы завершить регистрацию')
    else:
        form = UserRegisterForm()
    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid, )
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True  # устанавливаем поле is_active в значение True
        user.save()  # сохраняем изменения в базе данных
        return redirect(reverse_lazy('success_verify'))
        # return HttpResponse('Благодарим вас за подтверждение по электронной почте. '
        # 'Теперь вы можете войти в свою учетную запись.')
    else:
        return redirect(reverse_lazy('invalid_link'))
        # return HttpResponse('Ссылка для активации недействительна!')


def success_verify(request):
    return render(request, 'success_verify.html')


def invalid_link(request):
    return render(request, 'invalid_link.html')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
