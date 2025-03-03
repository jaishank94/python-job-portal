from django.contrib import admin
from .models import Lists, Company, Job

@admin.register(Lists)
class ListsAdmin(admin.ModelAdmin):
    list_display = ('type', 'description', 'is_on_homepage', 'created_at')
    list_filter = ('type', 'is_on_homepage')
    search_fields = ('description',)
    list_editable = ('is_on_homepage',)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'hq', 'employees', 'latest_funding_stage', 'rank')
    list_filter = ('latest_funding_stage', 'industries', 'lists')
    search_fields = ('name', 'description', 'industries')
    filter_horizontal = ('lists',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'website', 'description', 'rank')
        }),
        ('Location', {
            'fields': ('hq', 'offices')
        }),
        ('Company Details', {
            'fields': ('founded_date', 'employees', 'industries')
        }),
        ('Funding Information', {
            'fields': ('latest_funding_stage', 'total_funding_amount', 
                      'latest_funding_amount', 'latest_funding_date', 'valuation')
        }),
        ('People', {
            'fields': ('founders', 'investors')
        }),
        ('Lists', {
            'fields': ('lists',)
        }),
    )

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'level', 'location', 'is_remote', 'rank')
    list_filter = ('level', 'is_remote', 'lists')
    search_fields = ('title', 'company_name', 'description', 'skills', 'location')
    filter_horizontal = ('lists',)
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'company_name', 'description', 'url', 'rank')
        }),
        ('Experience & Level', {
            'fields': ('min_years_of_experience', 'max_years_of_experience', 'level')
        }),
        ('Compensation', {
            'fields': ('min_salary', 'max_salary')
        }),
        ('Job Details', {
            'fields': ('skills', 'location', 'is_remote')
        }),
        ('Lists', {
            'fields': ('lists',)
        }),
    )
