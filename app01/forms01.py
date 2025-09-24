from django import forms
from django.contrib.auth.models import User
from .models import Profile


class Form01(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name']
    def __init__(self, *args, **kwargs):
        super(Form01, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None  # au lieu de None
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Ton pseudo (tu peux mettre un emoji)',
        })

      
class Form02(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['badge']