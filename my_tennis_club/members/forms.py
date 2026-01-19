from django import forms
from .models import Member


class MemberForm(forms.ModelForm):
    """
    Form for creating and updating Member instances.
    Rails equivalent: form_for @member
    """
    class Meta:
        model = Member
        fields = ['firstname', 'lastname', 'email', 'phone']
        widgets = {
            'firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
        }

    def clean_email(self):
        """
        Custom validation for email field.
        Rails equivalent: validates :email, uniqueness: true
        """
        email = self.cleaned_data.get('email')
        # Check if email exists for a different member
        if Member.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

