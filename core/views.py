from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from pydantic import Json
from .serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Task, Employee
from .forms import AddEmployee

def home_view(request):
    if request.method == "POST":
        form = AddEmployee(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect('core:detail', instance.pk)
    else:
        form = AddEmployee()

    employees = Employee.objects.all().order_by('-name')
    context = {
        'form': form,
        'employees': employees
    }
    return render(request, 'core/home.html',  context)


def detail_view(request, id):
    employee = get_object_or_404(Employee, id=id)
    tasks = Task.objects.filter(employee=employee)
    context = {
        'employee': employee,
        'tasks': tasks
    }
    return render(request, 'core/detail.html', context)

# Api
@api_view(['GET', 'POST'])
def tasks_list(request):
    if request.method == 'GET':
        if 'employee' in request.query_params:
            tasks = Task.objects.filter(employee_id = request.query_params['employee'])
        else:
            tasks = Task.objects.all()
            
        if 'sort' in request.query_params:
            if request.query_params['sort'] == 'status':
                tasks = tasks.order_by('status')
                
            if request.query_params['sort'] =='-status':
                tasks = tasks.order_by('-status')
                
            if request.query_params['sort'] =='date':
                tasks = tasks.order_by('prediction')
                
            if request.query_params['sort'] == '-date':
                tasks = tasks.order_by('-prediction')

        tasks_serializer = TaskSerializer(tasks, many=True)
        return Response(tasks_serializer.data) 
    
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
    

@api_view(['GET', 'POST', 'PUT', 'DEL'])
def task(request, id):
    task = Task.objects.fillter(id=id)
    return Response()

        

