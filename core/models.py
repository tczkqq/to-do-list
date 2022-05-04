from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500, blank=True)
    

class Task(models.Model):
    
    class Status(models.IntegerChoices):
        NEW = 1, 'Nowe'
        COMPLETED = 2, 'Zrealizowane'
        
    class Category(models.IntegerChoices):
        FRONT = 1, 'FrontEnd'
        BACK = 2, 'BackEnd'
    
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    prediction = models.DateField()
    status = models.IntegerField(
        choices=Status.choices,
        default=1
    )
    # TODO: Category as manytomany
    category = models.IntegerField(choices=Category.choices, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    


    
