from django import forms
from .models import ContactRequest

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'phone', 'company_name', 'message', 'card_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number (optional)'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name (optional)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about your needs', 'rows': 4}),
            'card_type': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'card_type': 'What type of business card do you need?',
        }
