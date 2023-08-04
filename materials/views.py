from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from materials.models import Materials


class MaterialCreateView(CreateView):
    model = Materials
    fields = ('title', 'body')
    success_url = reverse_lazy('materials:list')


class MaterialUpdateView(UpdateView):
    model = Materials
    fields = ('title', 'body')
    success_url = reverse_lazy('materials:list')


class MaterialListView(ListView):
    model = Materials


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

