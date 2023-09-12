from django import forms

from catalog.models import Product, Subject


class FormStyleMixin:
    def __init__(self, **args):
        super().__init__(**args)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ProductForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ('name', 'description', 'email')
        # exclude = ('availability',)

    def clean_email(self):
        cleaned_data = self.cleaned_data['email']

        if cleaned_data:
            if not cleaned_data.endswith('@') and '@' not in cleaned_data:
                raise forms.ValidationError('Должен быть введен адрес почты ')
        else:
            raise forms.ValidationError('Должен быть введен адрес почты ')
        return cleaned_data

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']

        exception_words = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                           'обман', 'полиция', 'радар')
        for word in cleaned_data.split():
            if word.lower() in exception_words:
                raise forms.ValidationError('Такое слово нельзя вводить !!!')

        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']

        exception_words = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно',
                           'обман', 'полиция', 'радар')
        for word in cleaned_data.split():
            if word.lower() in exception_words:
                raise forms.ValidationError('Такое слово нельзя вводить !!!')

        return cleaned_data


class SubjectForm(FormStyleMixin, forms.ModelForm):
    class Meta:
        model = Subject
        fields = '__all__'
