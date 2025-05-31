from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()
from django import forms
from .models import Profile


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Имя или никнейм'})
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'})
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль ещё раз'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует.")
        return email

from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'placeholder': 'Имя или никнейм',
            'class': 'form-control',
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Пароль',
            'class': 'form-control',
        })
    )

class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['is_freshman', 'is_nonresident', 'is_international',
                  'is_employed', 'work_intensity']
        widgets = {
            'work_intensity': forms.RadioSelect
        }
        labels = {
            'is_freshman': 'Я - первокурсник',
            'is_nonresident': 'Я - иногородний студент',
            'is_international': 'Я - иностранный студент',
            'is_employed': 'Я работаю',
            'work_intensity': 'Интенсивность работы'
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('is_international') and cleaned_data.get('is_nonresident'):
            raise forms.ValidationError("Иностранный студент не может быть иногородним")
        return cleaned_data


from django import forms
from .models import Profile



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo', 'is_freshman', 'is_nonresident',
                  'is_international', 'is_employed', 'work_intensity']
        widgets = {'work_intensity': forms.RadioSelect}
