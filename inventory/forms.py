# inventory/forms.py

from django import forms
from .models import Item, Transaction

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'barcode', 'category', 'quantity']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['item', 'quantity', 'transaction_type']

class BarcodeScanForm(forms.Form):
    barcode = forms.CharField(max_length=13)
