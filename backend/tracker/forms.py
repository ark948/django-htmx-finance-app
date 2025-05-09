from django import forms

from .models import Transaction, Category



class TransactionForm(forms.ModelForm):

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Amount must be a positive number.')
        return amount

    class Meta:
        model = Transaction
        fields = (
            'type',
            'amount',
            'date',
            'category', 
        )
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}) # html attributes
        }