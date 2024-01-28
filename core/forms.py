from django import forms
from django_countries import fields
from django_countries import widgets

VELAYATS = (
    ('A','Ahal'),
    ('M','Mary'),
    ('B','Balkan'),
    ('D','Dashoguz'),
    ('L','Lebap')
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Sakarcage etr, Goreldeli d/b',
        'class':'form-control',
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder':'Ylham koce, jay N10, oy N20',
        'class':'form-control',
    }))
    country = fields.CountryField(blank_label='(Select a country)').formfield(
        widget=widgets.CountrySelectWidget(attrs={
            'class':'form-select'
        })
    )

    save_info = forms.BooleanField(required=False)
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Rahmanberdi',
        'class': 'form-control',
    }))
    surname = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Hojanazarov',
        'class': 'form-control',
    }))
    velayat = forms.ChoiceField(choices=VELAYATS,widget=forms.Select(attrs={
        'class': 'form-select'
    }))
    phonenumber = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '+99365234564',
        'class': 'form-control',
    }))


class CouponForm(forms.Form):
    coupon = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Promo code',
        'aria-label':'Promo code',
        'aria-describedby':'button-addon2'
    }))

class RefundForm(forms.Form):
    ref_code = forms.CharField(max_length=20)
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows':4,
    }))
    email = forms.EmailField()