from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Feedback


class BootstrapFormMixin:
    """Mixin to add Bootstrap classes automatically."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = existing_class + ' form-control'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'name',
            'contact',
            'age',
            'gender',
            'profile_pic'
        )
        widgets = {
            'profile_pic': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
        return username


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'name',
            'email',
            'contact',
            'age',
            'gender',
            'profile_pic'
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contact': forms.TextInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'})
        }


# Feedback Form

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your feedback here...',
                'class': 'form-control shadow-sm rounded-3 border-primary',
                'style': 'resize:none; background: rgba(255, 255, 255, 0.8);',
            }),
        }
        labels = {
            'message': 'Your Feedback',
        }