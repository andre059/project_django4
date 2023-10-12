from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from users.apps import UsersConfig
from users.views import ProfileView, RegisterView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('success_verify/', views.success_verify, name='success_verify'),
    path('invalid_link/', views.invalid_link, name='invalid_link'),
    # path('signup/', views.signup, name='signup'),
    path('activate/<uidb64>[0-9A-Za-z]+<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}', views.activate, name='activate')
]
