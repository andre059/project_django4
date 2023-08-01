from django.urls import path

from catalog.apps import MainConfig
from catalog.views import contacts, ProductListView, ProductDetailView

app_name = MainConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/views/', ProductDetailView.as_view(), name='inc_products_detail')
]
