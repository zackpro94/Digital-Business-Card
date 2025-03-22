from django import forms
from .models import ContactRequest

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'email', 'phone', 'company_name', 'message', 'card_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' ', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ' ', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': ' ', 'required': True, 'style': 'height: 150px;'}),
            'card_type': forms.RadioSelect(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Your Email',
            'phone': 'Phone Number (optional)',
            'company_name': 'Company Name (optional)',
            'message': 'Your Message',
            'card_type': 'Card Type'
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mark required fields
        for field_name in self.fields:
            if field_name in ['name', 'email', 'message', 'card_type']:
                self.fields[field_name].required = True
            else:
                self.fields[field_name].required = False
