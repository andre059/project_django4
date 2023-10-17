from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.decorators import unauthenticated_user
from materials.forms import MaterialsForm
from materials.models import Materials


class MaterialCreateView(CreateView):
    model = Materials
    # fields = ('title', 'body')
    form_class = MaterialsForm
    success_url = reverse_lazy('materials:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()

        return super().form_valid(form)


class MaterialUpdateView(UpdateView):
    model = Materials
    # fields = ('title', 'body', 'preview')
    form_class = MaterialsForm
    success_url = reverse_lazy('materials:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.price)
            new_mat.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('materials:view', args=[self.kwargs.get('pk')])


class MaterialListView(ListView):
    model = Materials

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class MateriaDetailView(DetailView):
    model = Materials

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class MateriaDeleteView(DeleteView):
    model = Materials
    success_url = reverse_lazy('materials:list')


def toggle_activiti(request, pk):
    materials_item = get_object_or_404(Materials, pk=pk)
    if materials_item.is_active:
        materials_item.is_active = False
    else:
        materials_item.is_active = True

    materials_item.save()

    return redirect(reverse('materials:list'))


@unauthenticated_user
def listM(request):
    return render(request, 'materials/materials_list.html')
