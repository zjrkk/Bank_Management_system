from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    # 将金额从元转换为分
    amount = forms.DecimalField(
        label='金额(元)',
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'}))

    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount', 'description', 'status', 'counterparty', 'counterparty_account']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        return int(amount * 100)  # 转换为分存储