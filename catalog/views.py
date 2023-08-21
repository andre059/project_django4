from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from pytils.translit import slugify

from catalog.forms_catalog import ProductForm, SubjectForm
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

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:view', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        SubjectFormset = inlineformset_factory(Product, Subject, form=SubjectForm, extra=2)
        context_data['formset'] = SubjectFormset()
        return context_data


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:home')
