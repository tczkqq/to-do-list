from django.forms import ModelForm
from . import models


class AddEmployee(ModelForm):
    class Meta:
        model = models.Employee
        fields = [
            'name',
            'description',
        ]
