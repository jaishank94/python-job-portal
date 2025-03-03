from django.core.management.base import BaseCommand
from job_app.models import Company, Job, Lists
from faker import Faker
import random
from datetime import datetime, timedelta
import decimal

class Command(BaseCommand):
    help = 'Populate database with random data'

    def handle(self, *args, **kwargs):
        fake = Faker()
        
        # Lists for random data
        industries = ['Artificial Intelligence', 'Blockchain', 'Cloud Computing', 'Data Analytics', 
                     'E-commerce', 'FinTech', 'Healthcare Tech', 'IoT', 'Machine Learning', 
                     'Mobile Apps', 'Robotics', 'SaaS', 'Security', 'Social Media']
        
        funding_stages = ['Seed', 'Series A', 'Series B', 'Series C', 'Series D', 'IPO']
        
        job_levels = ['Intern', 'Entry Level', 'Junior', 'Mid Level', 'Senior', 'Lead', 
                     'Manager', 'Director', 'VP', 'C-Level']
        
        skills = ['Python', 'JavaScript', 'Java', 'C++', 'React', 'Node.js', 'AWS', 'Docker', 
                 'Kubernetes', 'SQL', 'NoSQL', 'Machine Learning', 'Data Science', 'DevOps']

        # Create 50 companies
        for _ in range(50):
            num_employees = random.choice([10, 50, 100, 500, 1000, 5000, 10000])
            total_funding = random.randint(100000, 100000000)
            latest_funding = random.randint(50000, total_funding)
            
            company = Company.objects.create(
                name=fake.company(),
                description=fake.text(max_nb_chars=500),
                industries=', '.join(random.sample(industries, random.randint(1, 3))),
                website=fake.url(),
                hq=f"{fake.city()}, {fake.country()}",
                offices=f"{fake.city()}, {fake.city()}, {fake.city()}",
                founded_date=fake.date_between(start_date='-20y', end_date='-1y'),
                employees=num_employees,
                latest_funding_stage=random.choice(funding_stages),
                total_funding_amount=total_funding,
                latest_funding_amount=latest_funding,
                latest_funding_date=fake.date_between(start_date='-2y', end_date='today'),
                founders=', '.join([fake.name() for _ in range(random.randint(1, 3))]),
                investors=', '.join([fake.company() for _ in range(random.randint(2, 5))]),
                valuation=random.randint(1000000, 1000000000),
                rank=random.randint(1, 100)
            )
            
            # Create 1-3 jobs for each company
            for _ in range(random.randint(1, 3)):
                min_salary = random.randint(40000, 200000)
                max_salary = min_salary + random.randint(10000, 50000)
                min_yoe = random.randint(0, 5)
                max_yoe = min_yoe + random.randint(1, 5)
                
                Job.objects.create(
                    title=fake.job(),
                    company_name=company.name,
                    description=fake.text(max_nb_chars=1000),
                    location=f"{fake.city()}, {fake.country()}",
                    min_salary=min_salary,
                    max_salary=max_salary,
                    min_years_of_experience=min_yoe,
                    max_years_of_experience=max_yoe,
                    is_remote=random.choice([True, False]),
                    url=fake.url(),
                    skills=', '.join(random.sample(skills, random.randint(3, 6))),
                    level=random.choice(job_levels),
                    rank=random.randint(1, 100)
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated database with random data')) 