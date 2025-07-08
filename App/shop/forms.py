from django import forms
from .models import *


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['text', 'score']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': '10',
                'cols': '50',
                'maxlength': '1000',
            }),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['slug', 'title', 'img', 'description', 'shortdescription', 'price', 'provider', 'animal_sort', 'subcategory']
