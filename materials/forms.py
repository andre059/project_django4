from django import forms

from materials.models import Materials


class MaterialsForm(forms.ModelForm):
    class Meta:
        model = Materials
        fields = '__all__'
        # fields = ('title', 'body')
        # exclude = ('is_active',)
