from django.forms import ModelForm
from django import forms
from . import models


class AddEmployee(ModelForm):
    class Meta:
        model = models.Employee
        fields = [
            'name',
            'description',
        ]
        labels = {
            'name': "Imię i nazwisko",
            'description': "Opis"
        }
        widgets = {
    
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'})
        }
