
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_page, name='register_page'),
    path('login/', views.login_page, name='login_page'),
    path('', views.upload_file, name='main_page'),
    path('emp_login/', views.employee_login_page, name='employee_login_page'),
    path('dashboard/', views.dashboard_page, name='dashboard'),
    path('delete_employee/<int:id>/', views.delete_employee, name='delete_employee'),
    path('<int:id>/', views.update_emp, name='update_emp'),
    path('search_results/', views.search_results, name='search_results'),
    path('logout_view/', views.logout_view, name='logout_view'),

    


]