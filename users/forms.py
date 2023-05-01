from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    age = forms.IntegerField()
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('age','username', 'email')
    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age and age < 13:
            raise forms.ValidationError("You must be 13+ years old")
        return age
    
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields