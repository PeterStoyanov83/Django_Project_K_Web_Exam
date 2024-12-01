import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from client_management.models import CustomUser, Client, ClientFile, Laptop
from course_management.models import Course, CourseSchedule, Room, TimeSlot

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with random believable data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Create 5 rooms
        rooms = []
        min_room_capacity = float('inf')
        for i in range(1, 6):
            capacity = random.randint(20, 50)
            room = Room.objects.create(
                name=f'Room {i}',
                capacity=capacity
            )
            rooms.append(room)
            min_room_capacity = min(min_room_capacity, capacity)

        # Create 30 users (20 clients, 10 lecturers)
        users = []
        clients = []
        lecturers = []

        for i in range(30):
            user = CustomUser.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number(),
                address=fake.address(),
                date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=80)
            )
            users.append(user)

            if i < 20:  # First 20 users are clients
                client = Client.objects.create(
                    user=user,
                    company_name=fake.company(),
                    industry=fake.job()
                )
                clients.append(client)

                # Create ClientFiles (1-3 per client)
                for _ in range(random.randint(1, 3)):
                    ClientFile.objects.create(
                        client=client,
                        file=f'client_files/{fake.file_name(extension="pdf")}',
                        upload_date=fake.date_time_this_year(tzinfo=timezone.get_current_timezone())
                    )

                # Create Laptops (for 70% of clients)
                if random.random() < 0.7:
                    Laptop.objects.create(
                        client=client,
                        brand=fake.company(),
                        model=fake.word(),
                        serial_number=fake.unique.random_number(digits=8),
                        purchase_date=fake.date_this_year(),
                        warranty_end_date=fake.date_between(start_date='+1y', end_date='+3y'),
                        status=random.choice(['active', 'maintenance', 'retired'])
                    )
            else:  # Last 10 users are lecturers
                lecturers.append(user)

        # Create 10 courses
        courses = []
        for _ in range(10):
            course = Course.objects.create(
                title=fake.catch_phrase(),
                description=fake.paragraph(),
                lecturer=random.choice(lecturers),
                capacity=random.randint(10, min_room_capacity)
            )
            courses.append(course)

        # Create TimeSlots
        time_slots = []
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
        for day in days:
            for hour in range(9, 17, 2):  # 9 AM to 5 PM, 2-hour slots
                time_slot = TimeSlot.objects.create(
                    day=day,
                    start_time=f'{hour:02d}:00',
                    end_time=f'{hour+2:02d}:00'
                )
                time_slots.append(time_slot)

        # Create CourseSchedules
        for course in courses:
            for _ in range(random.randint(2, 5)):
                room = random.choice(rooms)
                while room.capacity < course.capacity:
                    room = random.choice(rooms)
                CourseSchedule.objects.create(
                    course=course,
                    room=room,
                    time_slot=random.choice(time_slots),
                    date=fake.date_between(start_date='today', end_date='+3m'),
                    status=random.choice(['SCHEDULED', 'CANCELLED', 'COMPLETED'])
                )

        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created {CustomUser.objects.count()} users'))
        self.stdout.write(self.style.SUCCESS(f'Created {Client.objects.count()} clients'))
        self.stdout.write(self.style.SUCCESS(f'Created {Laptop.objects.count()} laptops'))
        self.stdout.write(self.style.SUCCESS(f'Created {ClientFile.objects.count()} client files'))
        self.stdout.write(self.style.SUCCESS(f'Created {Course.objects.count()} courses'))
        self.stdout.write(self.style.SUCCESS(f'Created {CourseSchedule.objects.count()} course schedules'))
        self.stdout.write(self.style.SUCCESS(f'Created {Room.objects.count()} rooms'))
        self.stdout.write(self.style.SUCCESS(f'Created {TimeSlot.objects.count()} time slots'))

