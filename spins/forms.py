from django import forms
from .models import Spin

class SpinForm(forms.ModelForm):
    class Meta:
        model = Spin
        fields = ['caption', 'image']
      