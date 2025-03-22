from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('card/<uuid:uuid>/', views.card_detail, name='card_detail'),
    path('card/<uuid:uuid>/share/', views.card_share, name='card_share'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/companies/', views.company_list, name='company_list'),
    path('dashboard/companies/add/', views.company_create, name='company_create'),
    path('dashboard/companies/<int:pk>/edit/', views.company_edit, name='company_edit'),
    path('dashboard/companies/<int:pk>/delete/', views.company_delete, name='company_delete'),
    path('dashboard/employees/', views.employee_list, name='employee_list'),
    path('dashboard/employees/add/', views.employee_create, name='employee_create'),
    path('dashboard/employees/<int:pk>/edit/', views.employee_edit, name='employee_edit'),
    path('dashboard/employees/<int:pk>/delete/', views.employee_delete, name='employee_delete'),
    path('dashboard/individuals/', views.individual_list, name='individual_list'),
    path('dashboard/individuals/add/', views.individual_create, name='individual_create'),
    path('dashboard/individuals/<int:pk>/edit/', views.individual_edit, name='individual_edit'),
    path('dashboard/individuals/<int:pk>/delete/', views.individual_delete, name='individual_delete'),
    path('dashboard/cards/', views.card_list, name='card_list'),
    path('dashboard/cards/add/', views.card_create, name='card_create'),
    path('dashboard/cards/<int:pk>/edit/', views.card_edit, name='card_edit'),
    path('dashboard/cards/<int:pk>/delete/', views.card_delete, name='card_delete'),
    path('dashboard/analytics/', views.analytics, name='analytics'),
    path('dashboard/contact-requests/', views.contact_request_list, name='contact_request_list'),
    path('dashboard/contact-requests/<int:pk>/update-status/', views.contact_request_update_status, name='contact_request_update_status'),
]
