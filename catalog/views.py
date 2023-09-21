import glob
import webbrowser

from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from pytils.translit import slugify

from catalog.forms import ProductForm, SubjectForm
from catalog.models import Product, Subject


class ProductListView(ListView):
    model = Product


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


class ProductCreateView(CreateView):
    model = Product
    # fields = ('name', 'description', 'image', 'category', 'purchase_price')
    form_class = ProductForm
    success_url = reverse_lazy('catalog:home')


class ProductUpdateView(UpdateView):
    model = Product
    # fields = ('name', 'description', 'category')
    form_class = ProductForm
    template_name = 'catalog/product_form_with_formset.html'
    # success_url = reverse_lazy('catalog:home')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = None

    def get_success_url(self):
        return reverse('catalog:inc_products_detail', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Product, Subject, form=SubjectForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = SubjectFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = SubjectFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
            # new_mat = form.save()
            # new_mat.slug = slugify(new_mat.title)
            # new_mat.save()

        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')


def open_images(request):
    # Путь к папке с изображениями
    folder_path = "media/preview"

    # Поиск всех изображений в папке
    image_files = glob.glob(folder_path + "/*")
    # Одно изображение
    # image_files = ["media/preview"]

    # Передача списка изображений в шаблон
    return render(request, 'catalog/product_foto.html', {'image_files': image_files})

    # Открытие каждого изображения в браузере
    # for image_file in image_files:
    # return webbrowser.open(image_file)
