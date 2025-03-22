from django.contrib import admin
from .models import Company, Employee, IndividualClient, BusinessCard

# Register your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'website', 'created_at')
    search_fields = ('name', 'email')
    list_filter = ('created_at',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'job_title', 'email', 'phone', 'created_at')
    list_filter = ('company', 'created_at')
    search_fields = ('name', 'email', 'company__name')


@admin.register(IndividualClient)
class IndividualClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'job_title', 'email', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email')


@admin.register(BusinessCard)
class BusinessCardAdmin(admin.ModelAdmin):
    list_display = ('get_card_name', 'views', 'shares', 'last_viewed', 'created_at')
    list_filter = ('created_at', 'last_viewed')
    readonly_fields = ('views', 'shares', 'last_viewed', 'qr_code')
    
    def get_card_name(self, obj):
        if obj.employee:
            return f"{obj.employee.name} - {obj.employee.company.name}"
        elif obj.individual_client:
            return f"{obj.individual_client.name}"
        return "Unassigned Card"
    
    get_card_name.short_description = 'Card Owner'
