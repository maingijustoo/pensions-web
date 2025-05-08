from django import forms
from .models import Dependents

class AdminAddDependentForm(forms.ModelForm):
    class Meta:
        model = Dependents
        fields = ['dependentname', 'dateofbirth', 'relationship']
        widgets = {
            'dateofbirth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'dependentname': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control'})
        }