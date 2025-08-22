from django import forms
from .models import OrderStatus

class OrderItemStatusForm(forms.Form):
    status = forms.ModelChoiceField(queryset=OrderStatus.objects.all())
