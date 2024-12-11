import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from client_management.models import Client, ClientFile, Laptop
from course_management.models import Course, CourseSchedule, Resource

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with random believable users and related data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Number of users to create')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        self.stdout.write(self.style.SUCCESS(f'Creating {total} users...'))

        for _ in range(total):
            # Create User
            username = fake.user_name()
            email = fake.email()
            password = fake.password()
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            client = Client.objects.create(
                name=fake.name(),
                location=fake.city(),
                agreement_status=random.choice([True, False])
            )


            ClientFile.objects.create(
                client=client,
                file=f'client_files/{fake.file_name()}'
            )

            if random.choice([True, False]):
                Laptop.objects.create(
                    identifier=f'LAP-{fake.unique.random_number(digits=5)}',
                    client=client,
                    assigned_date=fake.date_this_year(),
                    return_date=fake.date_this_year(after_today=True)
                )

            course = Course.objects.create(
                name=fake.catch_phrase(),
                description=fake.paragraph(),
                platform=random.choice(['online', 'in_person', 'other'])
            )
            course.clients.add(client)

            CourseSchedule.objects.create(
                course=course,
                day_of_week=random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']),
                time_slot=fake.time()
            )

            Resource.objects.create(
                course=course,
                client=client,
                room=f'Room-{fake.building_number()}',
                seat=f'Seat-{fake.random_letter().upper()}{fake.random_digit()}'
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} users with related data!'))

