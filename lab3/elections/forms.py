from django import forms
from .models import County

class CountyForm(forms.ModelForm):
    class Meta:
        model = County
        fields = ["name", "state"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "County name"}),
        }
