from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Lists, Company, Job
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from datetime import datetime

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': 'jane.doe@school.edu'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': '••••••••••'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'input-field',
            'placeholder': '••••••••••'
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('jobs')
    else:
        form = CustomUserCreationForm()
    return render(request, 'job_app/register.html', {'form': form})

def home(request):
    # Get lists that are marked for homepage display
    company_lists = Lists.objects.filter(type='COMPANY', is_on_homepage=True)
    job_lists = Lists.objects.filter(type='JOB', is_on_homepage=True)
    
    return render(request, 'job_app/home.html', {
        'company_lists': company_lists,
        'job_lists': job_lists
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error = "Invalid email or password"
            return render(request, 'job_app/login.html', {'error': error})
    
    return render(request, 'job_app/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def item_detail(request, item_id):
    item = get_object_or_404(Lists, id=item_id)
    return render(request, 'job_app/item_detail.html', {
        'item': item
    })

def list_detail(request, list_id):
    list_obj = get_object_or_404(Lists, id=list_id)
    
    # Get companies and jobs for this list
    companies = list_obj.company_set.all().order_by('rank', 'name')
    jobs = list_obj.job_set.all().order_by('rank', '-created_at')
    
    # Get all unique company names for the dropdown
    all_company_names = Company.objects.values_list('name', flat=True).distinct().order_by('name')
    
    # Company filters
    company_filters = {
        'name': request.GET.get('company_name', ''),
        'industry': request.GET.get('industry', ''),
        'funding_stage': request.GET.get('funding_stage', ''),
        'founded_date': request.GET.get('founded_date', ''),
        'last_funding_amount': request.GET.get('last_funding_amount', ''),
        'total_funding_amount': request.GET.get('total_funding_amount', ''),
        'founders': request.GET.get('founders', ''),
        'headquarters': request.GET.get('headquarters', ''),
        'investors': request.GET.get('investors', ''),
        'description': request.GET.get('description', ''),
        'min_employees': request.GET.get('min_employees', ''),
        'max_employees': request.GET.get('max_employees', ''),
    }

    # Job filters
    job_filters = {
        'title': request.GET.get('job_title', ''),
        'location': request.GET.get('location', ''),
        'level': request.GET.get('level', ''),
        'skills': request.GET.get('skills', ''),
        'description': request.GET.get('description', ''),
        'is_remote': request.GET.get('is_remote', '') == 'on',
        'min_salary': request.GET.get('min_salary', ''),
        'max_salary': request.GET.get('max_salary', ''),
    }

    # Apply company filters
    if company_filters['name']:
        companies = companies.filter(name=company_filters['name'])
    if company_filters['industry']:
        companies = companies.filter(industries__icontains=company_filters['industry'])
    if company_filters['funding_stage']:
        companies = companies.filter(latest_funding_stage__icontains=company_filters['funding_stage'])
    if company_filters['founded_date']:
        try:
            companies = companies.filter(founded_date__year=int(company_filters['founded_date']))
        except ValueError:
            pass
    if company_filters['last_funding_amount']:
        try:
            amount = float(company_filters['last_funding_amount'])
            companies = companies.filter(last_funding_amount__gte=amount)
        except ValueError:
            pass
    if company_filters['total_funding_amount']:
        try:
            amount = float(company_filters['total_funding_amount'])
            companies = companies.filter(total_funding_amount__gte=amount)
        except ValueError:
            pass
    if company_filters['founders']:
        companies = companies.filter(founders__icontains=company_filters['founders'])
    if company_filters['headquarters']:
        companies = companies.filter(headquarters__icontains=company_filters['headquarters'])
    if company_filters['investors']:
        companies = companies.filter(investors__icontains=company_filters['investors'])
    if company_filters['description']:
        companies = companies.filter(description__icontains=company_filters['description'])
    if company_filters['min_employees']:
        try:
            companies = companies.filter(employees__gte=int(company_filters['min_employees']))
        except ValueError:
            pass
    if company_filters['max_employees']:
        try:
            companies = companies.filter(employees__lte=int(company_filters['max_employees']))
        except ValueError:
            pass

    # Apply job filters
    if job_filters['title']:
        jobs = jobs.filter(title__icontains=job_filters['title'])
    if job_filters['location']:
        jobs = jobs.filter(location__icontains=job_filters['location'])
    if job_filters['level']:
        jobs = jobs.filter(level__icontains=job_filters['level'])
    if job_filters['skills']:
        jobs = jobs.filter(skills__icontains=job_filters['skills'])
    if job_filters['description']:
        jobs = jobs.filter(description__icontains=job_filters['description'])
    if job_filters['is_remote']:
        jobs = jobs.filter(is_remote=True)
    if job_filters['min_salary']:
        try:
            jobs = jobs.filter(min_salary__gte=int(job_filters['min_salary']))
        except ValueError:
            pass
    if job_filters['max_salary']:
        try:
            jobs = jobs.filter(max_salary__lte=int(job_filters['max_salary']))
        except ValueError:
            pass

    # Pagination
    page = request.GET.get('page', 1)
    per_page = 25
    
    if list_obj.type == 'COMPANY':
        paginator = Paginator(companies, per_page)
        items = paginator.get_page(page)
    else:
        paginator = Paginator(jobs, per_page)
        items = paginator.get_page(page)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if list_obj.type == 'COMPANY':
            html = render_to_string('job_app/includes/company_rows.html', {
                'companies': items
            })
        else:
            html = render_to_string('job_app/includes/job_rows.html', {
                'jobs': items
            })
        return JsonResponse({
            'html': html,
            'has_next': items.has_next(),
            'next_page': items.next_page_number() if items.has_next() else None
        })

    return render(request, 'job_app/list_detail.html', {
        'list': list_obj,
        'companies': items if list_obj.type == 'COMPANY' else None,
        'jobs': items if list_obj.type == 'JOB' else None,
        'company_filters': company_filters,
        'job_filters': job_filters,
        'all_company_names': all_company_names,
    })

def jobs_view(request):
    # Fetch company logos using a dictionary for quick lookup
    company_logos = dict(Company.objects.values_list('name', 'logo_url'))

    # Get all jobs and lists
    jobs = Job.objects.all().order_by('rank', '-created_at')
    
    # Get all job lists for the dropdown
    job_lists = Lists.objects.filter(type='JOB').order_by('description')
    
    # Job filters
    job_filters = {
        'list_id': request.GET.get('list_id', ''),  # Changed from job_list to list_id
        'title': request.GET.get('title', ''),  # Changed from job_title
        'company': request.GET.get('company', ''),
        'location': request.GET.get('location', ''),
        'level': request.GET.get('level', ''),
        'skills': request.GET.get('skills', ''),
        'description': request.GET.get('description', ''),
        'is_remote': request.GET.get('is_remote', '') == 'on',
        'min_salary': request.GET.get('min_salary', ''),
        'max_salary': request.GET.get('max_salary', ''),
        'min_years_experience': request.GET.get('min_years_experience', ''),
        'max_years_experience': request.GET.get('max_years_experience', ''),
    }

    # Filter jobs by list if selected
    if job_filters['list_id']:
        try:
            jobs = jobs.filter(lists__id=job_filters['list_id'])
        except ValueError:
            pass

    # Apply job filters
    if job_filters['title']:
        jobs = jobs.filter(title__icontains=job_filters['title'])
    if job_filters['company']:
        jobs = jobs.filter(company_name__icontains=job_filters['company'])
    if job_filters['location']:
        jobs = jobs.filter(location__icontains=job_filters['location'])
    if job_filters['level']:
        jobs = jobs.filter(level__icontains=job_filters['level'])
    if job_filters['skills']:
        jobs = jobs.filter(skills__icontains=job_filters['skills'])
    if job_filters['description']:
        jobs = jobs.filter(description__icontains=job_filters['description'])
    if job_filters['is_remote']:
        jobs = jobs.filter(is_remote=True)
    if job_filters['min_salary']:
        try:
            jobs = jobs.filter(min_salary__gte=int(job_filters['min_salary']))
        except ValueError:
            pass
    if job_filters['max_salary']:
        try:
            jobs = jobs.filter(max_salary__lte=int(job_filters['max_salary']))
        except ValueError:
            pass
    if job_filters['min_years_experience']:
        try:
            jobs = jobs.filter(min_years_of_experience__gte=int(job_filters['min_years_experience']))
        except ValueError:
            pass
    if job_filters['max_years_experience']:
        try:
            jobs = jobs.filter(max_years_of_experience__lte=int(job_filters['max_years_experience']))
        except ValueError:
            pass

    # Assign company logos to jobs manually
    for job in jobs:
        job.logo_url = company_logos.get(job.company_name, '')
        
    # Pagination
    page = request.GET.get('page', 1)
    per_page = 25
    paginator = Paginator(jobs, per_page)
    items = paginator.get_page(page)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('job_app/includes/job_rows.html', {'jobs': items})
        return JsonResponse({'html': html, 'has_next': items.has_next()})

    return render(request, 'job_app/jobs.html', {
        'jobs': items,
        'job_filters': job_filters,
        'job_lists': job_lists,
    })

def companies_view(request):
    # Get all companies and lists
    companies = Company.objects.all().order_by('rank', 'name')
    
    # Get all company lists for the dropdown
    company_lists = Lists.objects.filter(type='COMPANY').order_by('description')
    
    # Company filters
    company_filters = {
        'list_id': request.GET.get('list_id', ''),
        'name': request.GET.get('name', ''),
        'description': request.GET.get('description', ''),
        'min_valuation': request.GET.get('min_valuation', ''),
        'max_valuation': request.GET.get('max_valuation', ''),
        'industry': request.GET.get('industry', ''),
        'funding_stage': request.GET.get('funding_stage', ''),
        'founded_date': request.GET.get('founded_date', ''),
        'min_latest_funding_amount': request.GET.get('min_latest_funding_amount', ''),
        'max_latest_funding_amount': request.GET.get('max_latest_funding_amount', ''),
        'min_latest_funding_date': request.GET.get('min_latest_funding_date', ''),
        'max_latest_funding_date': request.GET.get('max_latest_funding_date', ''),
        'total_funding_amount': request.GET.get('total_funding_amount', ''),
        'max_total_funding_amount': request.GET.get('max_total_funding_amount', ''),
        'founders': request.GET.get('founders', ''),
        'headquarters': request.GET.get('headquarters', ''),
        'offices': request.GET.get('offices', ''),
        'investors': request.GET.get('investors', ''),
    }

    # Filter companies by list if selected
    if company_filters['list_id']:
        try:
            selected_list = Lists.objects.get(id=company_filters['list_id'])
            companies = selected_list.company_set.all().order_by('rank', 'name')
        except Lists.DoesNotExist:
            pass

    # Apply other company filters
    if company_filters['name']:
        companies = companies.filter(name__icontains=company_filters['name'])
    if company_filters['description']:
        companies = companies.filter(description__icontains=company_filters['description'])
    if company_filters['min_valuation']:
        try:
            min_val = float(company_filters['min_valuation'])
            companies = companies.filter(valuation__gte=min_val)
        except ValueError:
            pass
    if company_filters['max_valuation']:
        try:
            max_val = float(company_filters['max_valuation'])
            companies = companies.filter(valuation__lte=max_val)
        except ValueError:
            pass
    if company_filters['industry']:
        companies = companies.filter(industries__icontains=company_filters['industry'])
    if company_filters['funding_stage']:
        companies = companies.filter(latest_funding_stage__icontains=company_filters['funding_stage'])
    if company_filters['min_latest_funding_amount']:
        try:
            min_amount = float(company_filters['min_latest_funding_amount'])
            companies = companies.filter(latest_funding_amount__gte=min_amount)
        except ValueError:
            pass
    if company_filters['max_latest_funding_amount']:
        try:
            max_amount = float(company_filters['max_latest_funding_amount'])
            companies = companies.filter(latest_funding_amount__lte=max_amount)
        except ValueError:
            pass
    if company_filters['min_latest_funding_date']:
        try:
            min_date = datetime.strptime(company_filters['min_latest_funding_date'], '%Y-%m-%d').date()
            companies = companies.filter(latest_funding_date__gte=min_date)
        except ValueError:
            pass
    if company_filters['max_latest_funding_date']:
        try:
            max_date = datetime.strptime(company_filters['max_latest_funding_date'], '%Y-%m-%d').date()
            companies = companies.filter(latest_funding_date__lte=max_date)
        except ValueError:
            pass
    if company_filters['total_funding_amount']:
        try:
            amount = float(company_filters['total_funding_amount'])
            companies = companies.filter(total_funding_amount__gte=amount)
        except ValueError:
            pass
    if company_filters['max_total_funding_amount']:
        try:
            amount = float(company_filters['max_total_funding_amount'])
            companies = companies.filter(total_funding_amount__lte=amount)
        except ValueError:
            pass
    if company_filters['founders']:
        companies = companies.filter(founders__icontains=company_filters['founders'])
    if company_filters['headquarters']:
        companies = companies.filter(hq__icontains=company_filters['headquarters'])
    if company_filters['offices']:
        companies = companies.filter(offices__icontains=company_filters['offices'])
    if company_filters['investors']:
        companies = companies.filter(investors__icontains=company_filters['investors'])

    # Pagination
    page = request.GET.get('page', 1)
    per_page = 25
    paginator = Paginator(companies, per_page)
    items = paginator.get_page(page)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render_to_string('job_app/includes/company_rows.html', {'companies': items})
        return JsonResponse({'html': html, 'has_next': items.has_next()})

    return render(request, 'job_app/companies.html', {
        'companies': items,
        'company_filters': company_filters,
        'company_lists': company_lists,
    })
