from django import forms
from django.contrib import messages
from django.db.models.fields import FieldDoesNotExist
from django.shortcuts import redirect
from django.utils.crypto import get_random_string

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from email_registration.views import USERNAME_FIELD
from pip._internal.utils._jaraco_text import _
from email_registration.utils import (InvalidCode, decode, send_registration_mail)
from email_registration.signals import password_set


from .forms import SignupForm, UserRegisterForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.translation import gettext_lazy

from django.shortcuts import render

from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from users.forms import UserProfileForm
from users.models import User
from .token import account_activation_token


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label=gettext_lazy('email address'),
        max_length=75,
        widget=forms.TextInput(attrs={
            'placeholder': gettext_lazy('email address'),
        }),
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError(_(
                'This email address already exists as an account.'
                ' Did you want to reset your password?'))
        return email


@require_POST
def email_registration_form(request, form_class=RegistrationForm):
    # TODO unajaxify this view for the release?
    form = form_class(request.POST)

    if form.is_valid():
        email = form.cleaned_data['email']
        send_registration_mail(email, request)

        return render(request, 'registration/email_registration_sent.html', {
            'email': email,
        })

    return render(request, 'registration/email_registration_form.html', {
        'form': form,
    })


def email_registration_confirm(request, code, max_age=3 * 86400,
                               form_class=SetPasswordForm):
    try:
        email, user = decode(code, max_age=max_age)
    except InvalidCode as exc:
        messages.error(request, '%s' % exc)
        return redirect('/')

    if not user:
        if User.objects.filter(email=email).exists():
            messages.error(request, _(
                'This email address already exists as an account.'
                ' Did you want to reset your password?'))
            return redirect('/')

        username_field = User._meta.get_field(USERNAME_FIELD)

        kwargs = {}
        if username_field.name == 'email':
            kwargs['email'] = email
        else:
            username = email

            # If email exceeds max length of field set username to random
            # string
            max_length = username_field.max_length
            if len(username) > max_length:
                username = get_random_string(
                    25 if max_length >= 25 else max_length)
            kwargs[username_field.name] = username

            # Set value for 'email' field in case the user model has one
            try:
                User._meta.get_field('email')
                kwargs['email'] = email
            except FieldDoesNotExist:
                pass

        user = User(**kwargs)

    if request.method == 'POST':
        form = form_class(user, request.POST)
        if form.is_valid():
            user = form.save()

            password_set.send(
                sender=user.__class__,
                request=request,
                user=user,
                password=form.cleaned_data.get('new_password1'),
            )

            messages.success(request, _(
                'Successfully set the new password. Please login now.'))

            return redirect('login')

    else:
        messages.success(request, _('Please set a password.'))
        form = form_class(user)

    return render(request, 'registration/password_set_form.html', {
        'form': form,
    })


# def signup(request):
    # if request.method == 'POST':
        # form = SignupForm(request.POST)
        # if form.is_valid():
            # save form in the memory not in database
            # user = form.save(commit=False)
            # user.is_active = False
            # user.save()
            # to get the domain of the current site
            # current_site = get_current_site(request)
            # mail_subject = 'Activation link has been sent to your email id'
            # message = render_to_string('acc_active_email.html', {
                # 'user': user,
                # 'domain': current_site.domain,
                # 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                # 'token': account_activation_token.make_token(user),
            # })
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(
                        # mail_subject, message, to=[to_email]
            # )
            # email.send()
            # return HttpResponse('Please confirm your email address to complete the registration')
    # else:
        # form = SignupForm()
    # return render(request, 'signup.html', {'form': form})


# # def activate(request, uidb64, token):
    # # User = get_user_model()
    # # try:
        # # uid = force_str(urlsafe_base64_decode(uidb64))
        # # user = User.objects.get(pk=uid)
    # # except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        # # user = None
    # # if user is not None and account_activation_token.check_token(user, token):
        # # user.is_active = True
        # # user.save()
        # # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    # # else:
        # # return HttpResponse('Activation link is invalid!')
