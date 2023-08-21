from django.urls import path

from catalog.apps import MainConfig
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductDeleteView, \
    ProductUpdateView

app_name = MainConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/views/', ProductDetailView.as_view(), name='inc_products_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='delete'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
]
