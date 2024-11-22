import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from faker import Faker
from client_management.models import Client, ClientFile, Laptop
from course_management.models import Course, CourseSchedule, Resource

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with random believable data'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Number of clients to create')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        self.stdout.write(self.style.SUCCESS(f'Creating {total} clients with related data...'))

        # Create Clients
        clients = []
        for _ in range(total):
            client = Client.objects.create(
                name=fake.name(),
                location=fake.city(),
                agreement_status=random.choice([True, False])
            )
            clients.append(client)

            # Create User for each Client
            User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=client.name.split()[0],
                last_name=client.name.split()[-1]
            )

            # Create ClientFiles (1-3 per client)
            for _ in range(random.randint(1, 3)):
                ClientFile.objects.create(
                    client=client,
                    file=f'client_files/{fake.file_name(extension="pdf")}',
                    uploaded_at=fake.date_time_this_year(tzinfo=timezone.get_current_timezone())
                )

        # Create Laptops (for 70% of clients)
        for client in random.sample(clients, k=int(total * 0.7)):
            Laptop.objects.create(
                identifier=f'LAP-{fake.unique.random_number(digits=5)}',
                client=client,
                assigned_date=fake.date_this_year(),
                return_date=fake.date_this_year(after_today=True)
            )

        # Create Courses
        courses = []
        for _ in range(total // 2):  # Create half as many courses as clients
            course = Course.objects.create(
                name=fake.catch_phrase(),
                description=fake.paragraph(),
                platform=random.choice(['online', 'in_person', 'other'])
            )
            courses.append(course)

            # Associate random clients with each course (3-10 clients per course)
            course_clients = random.sample(clients, k=random.randint(3, min(10, len(clients))))
            course.clients.set(course_clients)

            # Create CourseSchedules (2-5 per course)
            for _ in range(random.randint(2, 5)):
                CourseSchedule.objects.create(
                    course=course,
                    day_of_week=random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']),
                    time_slot=fake.time()
                )

        # Create Resources
        for course in courses:
            for client in course.clients.all():
                Resource.objects.create(
                    course=course,
                    client=client,
                    room=f'Room-{fake.building_number()}',
                    seat=f'Seat-{fake.random_letter().upper()}{fake.random_digit()}'
                )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} clients with related data!'))
        self.stdout.write(self.style.SUCCESS(f'Created {Course.objects.count()} courses'))
        self.stdout.write(self.style.SUCCESS(f'Created {CourseSchedule.objects.count()} course schedules'))
        self.stdout.write(self.style.SUCCESS(f'Created {Resource.objects.count()} resources'))
        self.stdout.write(self.style.SUCCESS(f'Created {Laptop.objects.count()} laptops'))
        self.stdout.write(self.style.SUCCESS(f'Created {ClientFile.objects.count()} client files'))
        self.stdout.write(self.style.SUCCESS(f'Created {User.objects.count()} users'))

