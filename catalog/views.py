import os

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from catalog.forms import ProductForm, SubjectForm, VersionForm
from catalog.models import Product, Subject, Version

from .decorators import unauthenticated_user


class ProductListView(ListView):
    model = Product


@login_required
def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        print(f'{name} ({email}): {message}')

    context = {
        'title': 'Контакты'
    }
    return render(request, 'catalog/contacts.html', context)


class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    permission_required = ['auth.is_staff', 'catalog.add_users']
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = ['auth.is_staff', 'catalog.change_users']
    template_name = 'catalog/product_form_with_formset.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_success_url(self):
        return reverse('catalog:inc_products_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        # Формирование формсета
        SubjectFormset = inlineformset_factory(Product, Subject, form=SubjectForm, extra=1)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['subject_formset'] = SubjectFormset(self.request.POST, instance=self.object)
            context_data['version_formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['subject_formset'] = SubjectFormset(instance=self.object)
            context_data['version_formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        subject_formset = self.get_context_data()['subject_formset']
        version_formset = self.get_context_data()['version_formset']

        self.object = form.save()

        if subject_formset.is_valid() and version_formset.is_valid():
            subject_formset.instance = self.object
            subject_formset.save()

            version_formset.instance = self.object
            version_formset.save()

            # new_mat = form.save()
            # new_mat.slug = slugify(new_mat.title)
            # new_mat.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        return self.request.user.is_superuser and self.request.user.is_staff


class ProductFotoView(View):
    def get(self, request):
        # Получение списка файлов из папки media/preview
        foto_dir = 'media/preview'  # Путь к папке с фотографиями
        foto_list = os.listdir(foto_dir)  # Список всех файлов в папке

        # Создание списка URL-адресов для каждой фотографии
        foto_urls = []
        for foto_file in foto_list:
            foto_path = os.path.join(foto_dir, foto_file)
            # Формируем URL, добавляя путь относительно корневой директории проекта
            foto_url = request.build_absolute_uri(f'/{foto_path}')
            foto_urls.append(foto_url)

        # Передача списка URL-адресов в шаблон
        context = {'foto_urls': foto_urls}

        return render(request, 'catalog/product_foto.html', context)


@login_required
def product_list_activ(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/product_is_active.html', context)


@unauthenticated_user
def home(request):
    return render(request, 'catalog/base.html')
