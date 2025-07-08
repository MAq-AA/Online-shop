from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField


class UserRegisterForm(UserCreationForm):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': 'Телефон'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'phone': forms.TextInput(attrs={'data-mask':"000-000-0000"}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': 'Электронная почта'})
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Пароль'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Повтор пароля'})


