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
    # path('activate/<str:uidb64>/<str:token>/', views.activate, name='activate'),
    path('success_verify/', views.success_verify, name='success_verify'),
    path('invalid_link/', views.invalid_link, name='invalid_link'),
    # path('users/verify-email/<uidb64>/<token>/', views.activate, name='verify-email'),
    # path('users/activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activate/<uidb64>[0-9A-Za-z]+<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20}', views.activate, name='activate')
]
