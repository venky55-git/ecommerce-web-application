from django import forms
from .models import ProductReview
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Product
from .models import CustomerAddress, Order  # project a


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    # Email field is already present in the User model, but to make sure it's included properly:
    email = forms.EmailField(required=True)  # Make email required

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']  # Explicitly include email field
    
    def clean_password2(self):
        # Check if password1 and password2 match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 != password2:
            raise ValidationError("The two password fields must match.")
        return password2
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        
        
# project a    ---------------------------------------------

class AddressForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = ['address_type', 'street', 'city', 'state', 'postal_code', 'country', 'is_default']
        widgets = {
            'street': forms.Textarea(attrs={'rows': 3}),
        }

class PaymentMethodForm(forms.Form):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
       # ('RAZORPAY', 'Razorpay'),
        #('PAYPAL', 'PayPal'),
    ]
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect,
        initial='COD'  # Set COD as default
    )
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'comment']        
      
        
# my account section---------------------------------------->
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = CustomerAddress
        fields = ['address_type', 'street', 'city', 'state', 'postal_code', 'country', 'is_default']
        widgets = {
            'address_type': forms.Select(attrs={'class': 'form-control'}),
            'street': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }
      