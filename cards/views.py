from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.http import JsonResponse
from .models import Company, Employee, IndividualClient, BusinessCard, ContactRequest
from django.forms import ModelForm, TextInput, EmailInput, URLInput, FileInput, Textarea, Select
from .forms import ContactRequestForm


# Create your views here.

# Forms
class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'logo', 'address', 'phone', 'email', 'website']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'address': Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'website': URLInput(attrs={'class': 'form-control'}),
        }


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['company', 'name', 'job_title', 'phone', 'email', 'profile_picture', 
                 'linkedin', 'twitter', 'facebook', 'instagram']
        widgets = {
            'company': Select(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'job_title': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'linkedin': URLInput(attrs={'class': 'form-control'}),
            'twitter': URLInput(attrs={'class': 'form-control'}),
            'facebook': URLInput(attrs={'class': 'form-control'}),
            'instagram': URLInput(attrs={'class': 'form-control'}),
        }


class IndividualClientForm(ModelForm):
    class Meta:
        model = IndividualClient
        fields = ['name', 'job_title', 'phone', 'email', 'website', 'profile_picture',
                 'linkedin', 'twitter', 'facebook', 'instagram']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'job_title': TextInput(attrs={'class': 'form-control'}),
            'phone': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'website': URLInput(attrs={'class': 'form-control'}),
            'linkedin': URLInput(attrs={'class': 'form-control'}),
            'twitter': URLInput(attrs={'class': 'form-control'}),
            'facebook': URLInput(attrs={'class': 'form-control'}),
            'instagram': URLInput(attrs={'class': 'form-control'}),
        }


class BusinessCardForm(ModelForm):
    class Meta:
        model = BusinessCard
        fields = ['employee', 'individual_client', 'theme']
        widgets = {
            'employee': Select(attrs={'class': 'form-control'}),
            'individual_client': Select(attrs={'class': 'form-control'}),
            'theme': Select(attrs={'class': 'form-control'})
        }


# Public views
def home(request):
    """Home page view with contact form."""
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your interest! We will contact you shortly.')
            return redirect('home')
    else:
        form = ContactRequestForm()
    
    context = {
        'form': form
    }
    return render(request, 'cards/home.html', context)


def card_detail(request, uuid):
    """Display a business card to the public."""
    card = get_object_or_404(BusinessCard, uuid=uuid)
    card.increment_view()
    
    if card.employee:
        context = {
            'card': card,
            'person': card.employee,
            'company': card.employee.company,
            'is_employee': True
        }
    else:
        context = {
            'card': card,
            'person': card.individual_client,
            'is_employee': False
        }
    
    # Determine which template to use based on the card's theme
    template_mapping = {
        'default': 'cards/card_detail.html',
        'elegant': 'cards/card_templates/elegant.html',
        'modern': 'cards/card_templates/modern.html',
    }
    
    template_name = template_mapping.get(card.theme, 'cards/card_detail.html')
    return render(request, template_name, context)


def card_share(request, uuid):
    """Increment share count and redirect to the card."""
    card = get_object_or_404(BusinessCard, uuid=uuid)
    card.increment_share()
    
    # Check if this is an AJAX request and return JSON if it is
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'shares': card.shares})
    
    # Otherwise redirect to the card detail page
    return redirect('card_detail', uuid=uuid)


# Admin dashboard views
@login_required
def dashboard(request):
    """Admin dashboard with summary statistics."""
    total_companies = Company.objects.count()
    total_employees = Employee.objects.count()
    total_individuals = IndividualClient.objects.count()
    total_cards = BusinessCard.objects.count()
    total_views = BusinessCard.objects.aggregate(Sum('views'))['views__sum'] or 0
    total_shares = BusinessCard.objects.aggregate(Sum('shares'))['shares__sum'] or 0
    
    # Get top 5 most viewed cards
    top_cards = BusinessCard.objects.order_by('-views')[:5]
    
    context = {
        'total_companies': total_companies,
        'total_employees': total_employees,
        'total_individuals': total_individuals,
        'total_cards': total_cards,
        'total_views': total_views,
        'total_shares': total_shares,
        'top_cards': top_cards,
    }
    
    return render(request, 'cards/dashboard.html', context)

# Company views
@login_required
def company_list(request):
    """List all companies."""
    companies = Company.objects.all()
    context = {
        'companies': companies
    }
    return render(request, 'cards/company_list.html', context)

@login_required
def company_create(request):
    """Create a new company."""
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company created successfully!')
            return redirect('company_list')
    else:
        form = CompanyForm()
    
    context = {
        'form': form,
        'title': 'Add Company'
    }
    return render(request, 'cards/company_form.html', context)

@login_required
def company_edit(request, pk):
    """Edit an existing company."""
    company = get_object_or_404(Company, pk=pk)
    
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company updated successfully!')
            return redirect('company_list')
    else:
        form = CompanyForm(instance=company)
    
    context = {
        'form': form,
        'title': 'Edit Company'
    }
    return render(request, 'cards/company_form.html', context)

@login_required
def company_delete(request, pk):
    """Delete a company."""
    company = get_object_or_404(Company, pk=pk)
    
    if request.method == 'POST':
        company.delete()
        messages.success(request, 'Company deleted successfully!')
        return redirect('company_list')
    
    context = {
        'company': company
    }
    return render(request, 'cards/company_confirm_delete.html', context)

# Employee views
@login_required
def employee_list(request):
    """List all employees."""
    employees = Employee.objects.all()
    context = {
        'employees': employees
    }
    return render(request, 'cards/employee_list.html', context)

@login_required
def employee_create(request):
    """Create a new employee."""
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee created successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm()
    
    context = {
        'form': form,
        'title': 'Add Employee'
    }
    return render(request, 'cards/employee_form.html', context)

@login_required
def employee_edit(request, pk):
    """Edit an existing employee."""
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee updated successfully!')
            return redirect('employee_list')
    else:
        form = EmployeeForm(instance=employee)
    
    context = {
        'form': form,
        'title': 'Edit Employee'
    }
    return render(request, 'cards/employee_form.html', context)

@login_required
def employee_delete(request, pk):
    """Delete an employee."""
    employee = get_object_or_404(Employee, pk=pk)
    
    if request.method == 'POST':
        employee.delete()
        messages.success(request, 'Employee deleted successfully!')
        return redirect('employee_list')
    
    context = {
        'employee': employee
    }
    return render(request, 'cards/employee_confirm_delete.html', context)

# Individual client views
@login_required
def individual_list(request):
    """List all individual clients."""
    individuals = IndividualClient.objects.all()
    context = {
        'individuals': individuals
    }
    return render(request, 'cards/individual_list.html', context)

@login_required
def individual_create(request):
    """Create a new individual client."""
    if request.method == 'POST':
        form = IndividualClientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Individual client created successfully!')
            return redirect('individual_list')
    else:
        form = IndividualClientForm()
    
    context = {
        'form': form,
        'title': 'Add Individual Client'
    }
    return render(request, 'cards/individual_form.html', context)

@login_required
def individual_edit(request, pk):
    """Edit an existing individual client."""
    individual = get_object_or_404(IndividualClient, pk=pk)
    
    if request.method == 'POST':
        form = IndividualClientForm(request.POST, request.FILES, instance=individual)
        if form.is_valid():
            form.save()
            messages.success(request, 'Individual client updated successfully!')
            return redirect('individual_list')
    else:
        form = IndividualClientForm(instance=individual)
    
    context = {
        'form': form,
        'title': 'Edit Individual Client'
    }
    return render(request, 'cards/individual_form.html', context)

@login_required
def individual_delete(request, pk):
    """Delete an individual client."""
    individual = get_object_or_404(IndividualClient, pk=pk)
    
    if request.method == 'POST':
        individual.delete()
        messages.success(request, 'Individual client deleted successfully!')
        return redirect('individual_list')
    
    context = {
        'individual': individual
    }
    return render(request, 'cards/individual_confirm_delete.html', context)

# Business card views
@login_required
def card_list(request):
    """List all business cards."""
    cards = BusinessCard.objects.all()
    context = {
        'cards': cards
    }
    return render(request, 'cards/card_list.html', context)

@login_required
def card_create(request):
    """Create a new business card."""
    if request.method == 'POST':
        form = BusinessCardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Business card created successfully!')
            return redirect('card_list')
    else:
        form = BusinessCardForm()
    
    context = {
        'form': form,
        'title': 'Add Business Card'
    }
    return render(request, 'cards/card_form.html', context)

@login_required
def card_edit(request, pk):
    """Edit an existing business card."""
    card = get_object_or_404(BusinessCard, pk=pk)
    
    if request.method == 'POST':
        form = BusinessCardForm(request.POST, instance=card)
        if form.is_valid():
            form.save()
            messages.success(request, 'Business card updated successfully!')
            return redirect('card_list')
    else:
        form = BusinessCardForm(instance=card)
    
    context = {
        'form': form,
        'title': 'Edit Business Card'
    }
    return render(request, 'cards/card_form.html', context)

@login_required
def card_delete(request, pk):
    """Delete a business card."""
    card = get_object_or_404(BusinessCard, pk=pk)
    
    if request.method == 'POST':
        card.delete()
        messages.success(request, 'Business card deleted successfully!')
        return redirect('card_list')
    
    context = {
        'card': card
    }
    return render(request, 'cards/card_confirm_delete.html', context)

@login_required
def analytics(request):
    """Display analytics for business cards."""
    # Get total views and shares
    total_views = BusinessCard.objects.aggregate(Sum('views'))['views__sum'] or 0
    total_shares = BusinessCard.objects.aggregate(Sum('shares'))['shares__sum'] or 0
    
    # Get top 10 most viewed cards
    top_viewed_cards = BusinessCard.objects.order_by('-views')[:10]
    
    # Get top 10 most shared cards
    top_shared_cards = BusinessCard.objects.order_by('-shares')[:10]
    
    # Get views and shares by month (last 6 months)
    # This would typically involve more complex queries with date filtering
    
    context = {
        'total_views': total_views,
        'total_shares': total_shares,
        'top_viewed_cards': top_viewed_cards,
        'top_shared_cards': top_shared_cards,
    }
    
    return render(request, 'cards/analytics.html', context)
