from django import forms

from .models import Transaction, Category



class TransactionForm(forms.ModelForm):
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