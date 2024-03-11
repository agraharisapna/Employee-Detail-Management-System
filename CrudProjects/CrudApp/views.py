from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import csv
import pandas as pd
from django.db.models import Q
from django.contrib.auth.decorators import login_required




# Create your views here.

@csrf_exempt

def register_page(request):

    if request.method == "POST":
        

        first_name   = request.POST.get('first_name')
        email = request.POST.get('email')
        password     = request.POST.get('password')
        designation  = request.POST.get('designation')
        user_dob    = request.POST.get('user_dob')
        date_joined  = request.POST.get('date_joined')
        gender  = request.POST.get('gender')
        imagess = request.FILES['imagess']
        role = request.POST.get('role')

        is_manager = True if role == 'Manager' else False
        is_employee = True if role == 'Employee' else False

        if gender == 'Male' or gender == 'Female' or gender == 'Others':
            gender = gender 
            print(gender , "gender")

        user_email = User.objects.filter(email=email)

        if user_email.exists():
            messages.error(request, "Your email is already registered.")
            return redirect("/register/")

        create_user = UserField.objects.create(
            username = first_name, password = password, user_designation = designation,
               birth_date = user_dob, date_joined = date_joined, user_gender = gender,
               images = imagess, is_employee=is_employee, is_manager=is_manager, email=email)
#
        create_user.set_password(password)
        create_user.save()

        messages.success(request, "Account created successfully !!")

        return redirect('/register/')

    return render(request, 'register.html')


@csrf_exempt
def login_page(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password     = request.POST.get('password')

        user_email = UserField.objects.filter(email = email)
        print("user---",user_email)

        if not user_email.exists():
            messages.error(request, "Email is not registered")
            return redirect('/login/')

        print(email, password)
        try:     
            user = authenticate(email=email, password=password)
            print(user)
        except Exception as e:
            print("Exception occurred:", e)

        # if user is None:
        #     print("Invalid User")
        #     messages.error(request, "Invalid User")
        #     return redirect('/login/')
        login(request, user)

        return redirect('dashboard')

    return render(request, 'login.html')


@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        if file.name.endswith('.csv'):
            # For CSV file
            data = csv.reader(file.read().decode('utf-8').splitlines())
            for row in data:
                username, email,password,date_joined, birth_date, user_gender, user_designation, is_manager, is_employee, images = row
                User.objects.create(username=username, email=email,password = password,date_joined=date_joined, birth_date= birth_date, user_gender= user_gender, user_designation = user_designation, is_manager= is_manager, is_employee= is_employee, images= images)
        elif file.name.endswith('.xlsx'):
            # For Excel file
            data = pd.read_excel(file)
            for _, row in data.iterrows():
                username, email, password,date_joined, birth_date, user_gender, user_designation, is_manager, is_employee, images = row['username'], row['email'], row['password'],row['date_joined'], row['birth_date'], row['user_gender'], row['user_designation'], row['is_manager'], row['is_employee'], row['images'] 
                User.objects.create(username=username, email=email,password = password,date_joined=date_joined, birth_date= birth_date, user_gender= user_gender, user_designation = user_designation, is_manager= is_manager, is_employee= is_employee, images= images)
        else:
            return render(request, 'error.html', {'error_message': 'Invalid file format'})
        return render(request, 'dashboard.html')
    return render(request, 'upload.html')




@csrf_exempt

def employee_login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = UserField.objects.filter(email=email).first()
        print(user)
        if user is None:
            messages.error(request, "Email is not registered")
            return redirect('/emp_login/')

        if user.is_employee:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Not a valid Employee Credential")
            return redirect('/emp_login/')

    return render(request, 'employeeLogin.html')

@login_required

def dashboard_page(request):
    employees = UserField.objects.all()
    return render(request, 'dashboard.html', {'employees': employees})

@login_required

def delete_employee(request, id):
    if request.method=="POST":
        user_del = UserField.objects.get(pk=id)    
        user_del.delete()
        return redirect('dashboard')
    
    return render(request, 'dashboard.html')

@login_required
    
def update_emp(request, id):
    user = UserField.objects.get(pk=id)

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')
        user_designation  = request.POST.get('user_designation')
    
        user.email = email
        user.password = password 
        user.user_designation = user_designation

        user.save()
    
        return redirect('dashboard')
        

    return render(request, 'updateEmp.html', {'user': user})

@login_required

def logout_view(request):
    logout(request)
    return redirect('/login/')

def search_results(request):
    query = request.GET.get('?')
    results = UserField.objects.filter(
        Q(username__icontains=query) |  
        Q(user_designation__icontains=query) 
        
    )
    return render(request, 'dashboard.html', {'results': results, 'query': query})