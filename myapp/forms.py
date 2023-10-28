from django import forms
from .models import Product


class ProductForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    age = forms.IntegerField(min_value=0, max_value=120)

    def clean_name(self):
        """Плохой пример. Подмена параметра min_length."""
        name = self.cleaned_data['name']
        if len(name) < 3:
            raise forms.ValidationError('Имя должно содержать неменее 3 символов')
        return name

    def clean_email(self):
        email: str = self.cleaned_data['email']
        if not (email.endswith('vk.team') or email.endswith('corp.mail.ru')):
            raise forms.ValidationError('Используйте корпоративную почту')
        return email


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'creation_date', 'photo']
        labels = {
            'name': 'Name',
            'description': 'Description',
            'price': 'Price',
            'quantity': 'Quantity',
            'creation_date': 'Creation Date',
            'photo': 'Photo',
        }
        widgets = {
            'creation_date': forms.DateInput(attrs={'type': 'date'}),
        }
