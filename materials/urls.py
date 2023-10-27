from django.urls import path
from django.views.decorators.cache import cache_page

# from .views import listM
from materials.apps import MaterialsConfig
from materials.views import MaterialCreateView, MaterialListView, MateriaDetailView, MaterialUpdateView, \
    MateriaDeleteView, toggle_activiti

app_name = MaterialsConfig.name

urlpatterns = [
    path('create/', MaterialCreateView.as_view(), name='create'),
    path('', cache_page(60)(MaterialListView.as_view()), name='list'),
    path('view/<int:pk>/', MateriaDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', MaterialUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', MateriaDeleteView.as_view(), name='delete'),
    path('activity/<int:pk>/', toggle_activiti, name='toggle_activiti'),
    # path('list/', listM, name='list'),
]
