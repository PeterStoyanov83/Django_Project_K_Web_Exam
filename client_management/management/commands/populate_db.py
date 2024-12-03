from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.contrib.auth import get_user_model
from faker import Faker
from client_management.models import CustomUser, Client, ClientFile, Laptop
from course_management.models import Course, CourseSchedule, Room, TimeSlot, CourseApplication
import random
from django.db.utils import IntegrityError

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with random believable data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-clean',
            action='store_true',
            help='Do not clean the database before populating',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not options['no_clean']:
            self.stdout.write(self.style.WARNING('Cleaning the database...'))
            call_command('clean_db')

        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        try:
            # Create 5 rooms
            rooms = self.create_rooms()

            # Create 30 users (20 clients, 10 lecturers)
            users, clients, lecturers = self.create_users()

            # Create 10 courses
            courses = self.create_courses(lecturers, rooms)

            # Create TimeSlots
            time_slots = self.create_time_slots()

            # Create CourseSchedules
            self.create_course_schedules(courses, rooms, time_slots)

            # Create CourseApplications
            self.create_course_applications(courses, clients)

            self.print_summary()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            raise

    def create_rooms(self):
        rooms = [Room.objects.create(name=f"Room {i}", capacity=random.randint(20, 100)) for i in range(1, 6)]
        return rooms

    def create_users(self):
        User = get_user_model()
        existing_superuser = User.objects.filter(is_superuser=True).first()
        users = []
        clients = []
        lecturers = []

        user_data = []
        client_data = []
        laptop_data = []
        client_file_data = []

        for i in range(30):
            if i == 0 and existing_superuser:
                users.append(existing_superuser)
                continue

            user = CustomUser(
                username=fake.user_name(),
                email=fake.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number()[:15],  # Truncate to 15 characters
                address=fake.address(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80)
            )
            user_data.append(user)

            if i < 20:  # First 20 users are clients
                client = Client(
                    user=user,
                    company_name=fake.company(),
                    industry=fake.job()
                )
                client_data.append(client)

                # Create ClientFiles (1-3 per client)
                for _ in range(random.randint(1, 3)):
                    client_file_data.append(ClientFile(
                        client=client,
                        file=f'client_files/{fake.file_name(extension="pdf")}',
                        uploaded_at=fake.date_time_this_year(tzinfo=timezone.get_current_timezone()),
                        uploaded_by=user
                    ))

                # Create Laptops (for 70% of clients)
                if random.random() < 0.7:
                    laptop_data.append(Laptop(
                        client=client,
                        brand=fake.company(),
                        model=fake.word(),
                        serial_number=fake.unique.random_number(digits=8),
                        purchase_date=fake.date_this_year(),
                        warranty_end_date=fake.date_between(start_date='+1y', end_date='+3y'),
                        status=random.choice(['active', 'maintenance', 'retired'])
                    ))
            else:  # Last 10 users are lecturers
                user.is_staff = True
                lecturers.append(user)

        # Bulk create users
        users = CustomUser.objects.bulk_create(user_data)

        # Bulk create clients
        clients = Client.objects.bulk_create(client_data)

        # Bulk create laptops
        Laptop.objects.bulk_create(laptop_data)

        # Bulk create client files
        ClientFile.objects.bulk_create(client_file_data)

        return users, clients, lecturers

    def create_courses(self, lecturers, rooms):
        courses = []
        for _ in range(10):
            room = random.choice(rooms)
            course = Course.objects.create(
                title=fake.catch_phrase(),
                description=fake.paragraph(),
                lecturer=random.choice(lecturers),
                capacity=random.randint(10, room.capacity)  # Ensure course capacity doesn't exceed room capacity
            )
            courses.append(course)
        return courses

    def create_time_slots(self):
        time_slot_data = []
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
        for day in days:
            for hour in range(9, 17, 2):  # 9 AM to 5 PM, 2-hour slots
                time_slot_data.append({
                    'day': day,
                    'start_time': f'{hour:02d}:00',
                    'end_time': f'{hour+2:02d}:00'
                })
        time_slots = TimeSlot.objects.bulk_create([TimeSlot(**data) for data in time_slot_data])
        return time_slots

    def create_course_schedules(self, courses, rooms, time_slots):
        for course in courses:
            for _ in range(random.randint(2, 5)):
                room = random.choice([r for r in rooms if r.capacity >= course.capacity])
                CourseSchedule.objects.create(
                    course=course,
                    room=room,
                    time_slot=random.choice(time_slots),
                    date=fake.date_between(start_date='today', end_date='+3m'),
                    status=random.choice(['SCHEDULED', 'CANCELLED', 'COMPLETED'])
                )

    def create_course_applications(self, courses, clients):
        application_data = []
        for course in courses:
            for _ in range(random.randint(5, 15)):
                client = random.choice(clients)
                application_data.append({
                    'user': client.user,
                    'course': course,
                    'status': random.choice(['pending', 'approved', 'rejected']),
                    'application_date': fake.date_time_this_year(tzinfo=timezone.get_current_timezone())
                })
        CourseApplication.objects.bulk_create([CourseApplication(**data) for data in application_data])

    def print_summary(self):
        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created {CustomUser.objects.count()} users'))
        self.stdout.write(self.style.SUCCESS(f'Created {Client.objects.count()} clients'))
        self.stdout.write(self.style.SUCCESS(f'Created {Laptop.objects.count()} laptops'))
        self.stdout.write(self.style.SUCCESS(f'Created {ClientFile.objects.count()} client files'))
        self.stdout.write(self.style.SUCCESS(f'Created {Course.objects.count()} courses'))
        self.stdout.write(self.style.SUCCESS(f'Created {CourseSchedule.objects.count()} course schedules'))
        self.stdout.write(self.style.SUCCESS(f'Created {Room.objects.count()} rooms'))
        self.stdout.write(self.style.SUCCESS(f'Created {TimeSlot.objects.count()} time slots'))
        self.stdout.write(self.style.SUCCESS(f'Created {CourseApplication.objects.count()} course applications'))

