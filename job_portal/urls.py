"""
URL configuration for job_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from job_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.jobs_view, name='jobs'),
    path('jobs/<slug:slug>/', views.jobs_view, name='jobs_by_slug'),
    path('companies/', views.companies_view, name='companies'),
    path('companies/<slug:slug>/', views.companies_view, name='companies_by_slug'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('list/<int:list_id>/', views.list_detail, name='list_detail'),
]
