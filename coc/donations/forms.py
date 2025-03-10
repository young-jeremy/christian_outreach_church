# donations/forms.py
from django import forms
from .models import DonationSettings
from django import forms
from .models import Donation, DonationSettings
from payments.models import PaymentMethod


class DonationForm(forms.ModelForm):
    """Form for making donations"""

    class Meta:
        model = Donation
        fields = ['amount', 'donation_type', 'recurring', 'notes']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.01',
                'step': '0.01',
                'placeholder': '0.00'
            }),
            'donation_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'recurring': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any special instructions or designations for this donation'
            })
        }
        labels = {
            'amount': 'Donation Amount',
            'donation_type': 'Donation Type',
            'recurring': 'Make this a recurring donation',
            'notes': 'Notes (Optional)'
        }

    def clean_amount(self):
        """Validate that the amount is positive"""
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError("Donation amount must be greater than zero.")
        return amount


class DonationSettingsForm(forms.ModelForm):
    """Form for donation settings"""

    class Meta:
        model = DonationSettings
        fields = [
            'recurring_tithe',
            'recurring_missions',
            'recurring_building_fund',
            'preferred_payment_method',
            'donation_receipts'
        ]
        widgets = {
            'recurring_tithe': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'recurring_missions': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'recurring_building_fund': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'preferred_payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),
            'donation_receipts': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'recurring_tithe': 'Set up recurring tithe',
            'recurring_missions': 'Set up recurring missions giving',
            'recurring_building_fund': 'Set up recurring building fund giving',
            'preferred_payment_method': 'Preferred Payment Method',
            'donation_receipts': 'Donation Receipts'
        }


class PaymentMethodForm(forms.ModelForm):
    """Form for payment methods"""

    class Meta:
        model = PaymentMethod
        fields = ['payment_type', 'is_default']
        widgets = {
            'payment_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'is_default': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
        labels = {
            'payment_type': 'Payment Type',
            'is_default': 'Set as default payment method'
        }

    # Credit card fields (not stored in the model)
    card_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXXX XXXX XXXX XXXX'
        }),
        label='Card Number'
    )

    expiry_date = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'MM/YY'
        }),
        label='Expiry Date'
    )

    cvv = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'XXX'
        }),
        label='CVV'
    )

    name_on_card = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label='Name on Card'
    )

    # Bank account fields (not stored in the model)
    account_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label='Account Holder Name'
    )

    routing_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label='Routing Number'
    )

    account_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        label='Account Number'
    )

    account_type = forms.ChoiceField(
        required=False,
        choices=[('checking', 'Checking'), ('savings', 'Savings')],
        widget=forms.Select(attrs={
            'class': 'form-select'
        }),
        label='Account Type'
    )

    def clean(self):
        """Validate form based on payment type"""
        cleaned_data = super().clean()
        payment_type = cleaned_data.get('payment_type')

        if payment_type == 'creditCard':
            card_number = cleaned_data.get('card_number')
            expiry_date = cleaned_data.get('expiry_date')
            cvv = cleaned_data.get('cvv')
            name_on_card = cleaned_data.get('name_on_card')

            if not card_number:
                self.add_error('card_number', 'Card number is required')

            if not expiry_date:
                self.add_error('expiry_date', 'Expiry date is required')

            if not cvv:
                self.add_error('cvv', 'CVV is required')

            if not name_on_card:
                self.add_error('name_on_card', 'Name on card is required')

        elif payment_type == 'bankAccount':
            account_name = cleaned_data.get('account_name')
            routing_number = cleaned_data.get('routing_number')
            account_number = cleaned_data.get('account_number')
            account_type = cleaned_data.get('account_type')

            if not account_name:
                self.add_error('account_name', 'Account holder name is required')

            if not routing_number:
                self.add_error('routing_number', 'Routing number is required')

            if not account_number:
                self.add_error('account_number', 'Account number is required')

            if not account_type:
                self.add_error('account_type', 'Account type is required')

        return cleaned_data
