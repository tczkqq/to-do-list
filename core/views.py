from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .serializers import TaskSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import csv

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


def export_csv(request, id):
    # TODO: Export friendly names for status and category
    employee = get_object_or_404(Employee, id=id)
    tasks = Task.objects.filter(employee=employee)
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + employee.name + '.csv'
    writer = csv.writer(response)
    writer.writerow([
        'ID', 
        'Name', 
        'Description', 
        'Created', 
        'Prediction',
        'Status',
        'Category'
    ])
    tsks = tasks.values_list(
        'id',
        'name',
        'description',
        'created',
        'prediction',
        'status',
        'category'
    )
    for t in tsks:
        writer.writerow(t)
    return response


# Api
@api_view(['GET', 'POST'])
def tasks_list(request):
    if request.method == 'GET':
        if 'employee' in request.query_params:
            tasks = Task.objects.filter(employee_id = request.query_params['employee'])
        else:
            tasks = Task.objects.all()
            
        if 'sort' in request.query_params:
            if request.query_params['sort'] == 'category':
                tasks = tasks.order_by('category')
                
            if request.query_params['sort'] =='-category':
                tasks = tasks.order_by('-category')
                
            if request.query_params['sort'] =='date':
                tasks = tasks.order_by('prediction')
                
            if request.query_params['sort'] == '-date':
                tasks = tasks.order_by('-prediction')

        tasks_serializer = TaskSerializer(tasks, many=True)
        return Response(tasks_serializer.data) 
    
    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        employee_id = request.data.get('employee') 
        employee = Employee.objects.get(id=employee_id)
        if serializer.is_valid():
            serializer.save(employee=employee)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(request.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)    
    
    
@api_view(['PATCH', 'DELETE'])
def task(request, id):
    task = Task.objects.get(id=id)
    if not task:
        return Response(status.HTTP_204_NO_CONTENT)
    
    if request.method == 'PATCH':
        task.status = request.data.get('status')
        task.save()
        return Response(status=status.HTTP_200_OK)
        
    if request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_200_OK)
        
    return Response()

        

