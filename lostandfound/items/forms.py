from django import forms
from .models import ReportedItem

class ReportForm(forms.ModelForm):
    class Meta:
        model = ReportedItem
        fields = ['type', 'name', 'description', 'location', 'contact', 'image']
