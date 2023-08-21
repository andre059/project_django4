from django import forms

from catalog.models import Product, Subject


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ('name', 'description')
        # exclude = ('availability',)


class SubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = '__all__'

