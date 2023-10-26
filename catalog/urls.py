from django.urls import path

from catalog import views
from catalog.apps import MainConfig
from catalog.views import contacts, ProductListView, ProductDetailView, ProductCreateView, ProductDeleteView, \
    ProductUpdateView, ProductFotoView

# from .views import home

app_name = MainConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/views/', ProductDetailView.as_view(), name='inc_products_detail'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='delete'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update'),
    path('product_foto/', ProductFotoView.as_view(), name='product_foto'),
    path('version/', views.product_list_activ, name='version'),
]
