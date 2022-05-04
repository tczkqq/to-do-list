from rest_framework import serializers
from . import models

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Task
        fields = [
            'id',
            'name',
            'description',
            'created',
            'prediction',
            'status',
            'category'
        ]