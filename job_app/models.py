from django.db import models

class Lists(models.Model):
    TYPE_CHOICES = [
        ('JOB', 'Job'),
        ('COMPANY', 'Company'),
    ]
    
    type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='JOB'
    )
    description = models.TextField()
    is_on_homepage = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.description)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'List'
        verbose_name_plural = 'Lists'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.type} - {self.description[:50]}"

class Company(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=255)
    hq = models.CharField(max_length=255, blank=True, null=True)
    offices = models.CharField(max_length=255, blank=True, null=True)
    founded_date = models.DateField(blank=True, null=True)
    latest_funding_stage = models.CharField(max_length=255, blank=True, null=True)
    total_funding_amount = models.IntegerField(default=0)
    latest_funding_amount = models.IntegerField(default=0)
    founders = models.CharField(max_length=255, blank=True, null=True)
    valuation = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    employees = models.IntegerField(default=0)
    investors = models.CharField(max_length=255, blank=True, null=True)
    latest_funding_date = models.DateField(blank=True, null=True)
    industries = models.CharField(max_length=255, blank=True, null=True)
    lists = models.ManyToManyField(Lists)
    rank = models.IntegerField(default=0)
    logo_url = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'
        ordering = ['rank', 'name']

    def __str__(self):
        return self.name

class Job(models.Model):
    title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=255)
    min_years_of_experience = models.IntegerField(blank=True, null=True)
    max_years_of_experience = models.IntegerField(blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    min_salary = models.IntegerField(blank=True, null=True)
    max_salary = models.IntegerField(blank=True, null=True)
    skills = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    lists = models.ManyToManyField(Lists)
    rank = models.IntegerField(default=0)
    company_logo = models.CharField(max_length=255, blank=True, null=True)
    is_remote = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['rank', '-created_at']

    def __str__(self):
        return self.title
