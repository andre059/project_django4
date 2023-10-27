from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.decorators import unauthenticated_user
from materials.forms import MaterialsForm
from materials.models import Materials
from materials.services import get_cached_for_materials


class MaterialCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Materials
    form_class = MaterialsForm
    permission_required = 'materials.add_users'
    success_url = reverse_lazy('materials:list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.name)
            new_mat.save()

        return super().form_valid(form)


class MaterialUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Materials
    form_class = MaterialsForm
    permission_required = 'materials.change_users'
    # success_url = reverse_lazy('materials:list')

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


class MateriaDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Materials
    permission_required = 'materials.view_users'

    def get_object(self, queryset=None):
        object = super().get_object(queryset)
        object.views_count = get_cached_for_materials(object.pk)
        return object

    # def get_context_data(self, **kwargs):
        # context_data = super().get_context_data(**kwargs)
        # if settings.CACHES_ENABLED:
            # key = f'subject_list{self.object.pk}'
            # subject_list = cache.get(key)
            # if subject_list is None:
                # subject_list = self.object.subject_set.all()
                # cache.set(key, subject_list)
        # else:
            # subject_list = self.object.subject_set.all()

        # context_data['subjects'] = subject_list
        # return context_data


class MateriaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Materials
    success_url = reverse_lazy('materials:list')

    def test_func(self):
        return self.request.user.is_superuser


@login_required
@permission_required('materials.view_user')
def toggle_activiti(request, pk):
    materials_item = get_object_or_404(Materials, pk=pk)
    if materials_item.is_active:
        materials_item.is_active = False
    else:
        materials_item.is_active = True

    materials_item.save()

    return redirect(reverse('materials:list'))


# @unauthenticated_user
# def listM(request):
    # return render(request, 'materials/materials_list.html')
