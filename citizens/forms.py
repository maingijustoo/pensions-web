from django import forms
from kua.models import Members

class CitizenRegistrationForm(forms.ModelForm):
    class Meta:
        model = Members
        fields = ['fullname', 'dateofbirth', 'contactnumber', 'email', 'address', 'nssfcardnumber', 'krapin', 'employerid']
        widgets = {
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'dateofbirth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'contactnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter contact number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter address'}),
            'nssfcardnumber': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter NSSF card number'}),
            'krapin': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter KRA PIN'}),
            'employerid': forms.Select(attrs={'class': 'form-control'}),
        }

