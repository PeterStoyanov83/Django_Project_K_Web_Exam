from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from faker import Faker
from client_management.models import CustomUser, Client
from course_management.models import Course, CourseSchedule, Room, TimeSlot, CourseApplication, Booking
import random
from datetime import timedelta
from django.core.exceptions import ValidationError

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
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        try:
            # Create rooms
            rooms = self.create_rooms()

            # Create users (20 clients, 10 lecturers)
            users, clients, lecturers = self.create_users()

            # Create 15 courses
            courses = self.create_courses(lecturers, rooms)

            # Create TimeSlots
            time_slots = self.create_time_slots()

            # Create CourseSchedules
            self.create_course_schedules(courses, rooms, time_slots)

            # Create Bookings
            self.create_bookings(users, courses)

            self.print_summary()
            return None

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))
            raise

    @staticmethod
    def create_rooms():
        rooms = []
        for i in range(1, 6):
            room = Room.objects.create(
                name=f"Room {i}",
                capacity=random.randint(20, 100)
            )
            rooms.append(room)
        return rooms

    @staticmethod
    def create_users():
        users = []
        clients = []
        lecturers = []

        for i in range(30):
            user = CustomUser.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password="password123",
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone_number=fake.phone_number()[:15],
                address=fake.address(),
                date_of_birth=fake.date_of_birth(
                    minimum_age=18,
                    maximum_age=80
                )
            )

            if i < 20:  # First 20 users are clients
                user.user_type = 'PRIVATE'
                client = Client.objects.create(
                    user=user,
                    company_name=fake.company(),
                    industry=fake.job()
                )
                clients.append(client)
            else:  # Last 10 users are lecturers
                user.is_staff = True
                user.user_type = 'BUSINESS'
                lecturers.append(user)

            user.save()
            users.append(user)

        return users, clients, lecturers

    def create_courses(self, lecturers, rooms):
        courses = []
        max_room_capacity = max(room.capacity for room in rooms)
        for i in range(15):
            lecturer = lecturers[i % 10]  # This ensures 5 lecturers teach 2 courses
            room = random.choice(rooms)
            course = Course.objects.create(
                title=fake.catch_phrase(),
                description=fake.paragraph(),
                lecturer=lecturer,
                room=room,
                capacity=random.randint(
                    10,
                    min(room.capacity, max_room_capacity))
            )
            if not course.calendar:
                from schedule.models import Calendar
                slug = f"course-{course.id}-calendar"
                course.calendar = Calendar.objects.create(
                    name=f"Calendar for {course.title}",
                    slug=slug
                )
                course.save()
            courses.append(course)
        return courses

    @staticmethod
    def create_time_slots():
        created_time_slots = []
        days = ['MON', 'TUE', 'WED', 'THU', 'FRI']
        for day in days:
            for hour in range(9, 18, 3):  # 9 AM to 6 PM, 3-hour slots
                start_time = timezone.datetime.strptime(f'{hour:02d}:00', '%H:%M').time()
                end_time = timezone.datetime.strptime(f'{(hour + 3):02d}:00', '%H:%M').time()
                time_slot = TimeSlot.objects.create(
                    day=day,
                    start_time=start_time,
                    end_time=end_time
                )
                created_time_slots.append(time_slot)
        return created_time_slots

    def create_course_schedules(self, courses, rooms, time_slots):
        for course in courses:
            start_date = timezone.now().date() + timedelta(days=random.randint(1, 30))
            for _ in range(random.randint(5, 10)):  # 5-10 schedules per course
                # Filter rooms with sufficient capacity
                suitable_rooms = [room for room in rooms if room.capacity >= course.capacity]
                if not suitable_rooms:
                    continue  # Skip this schedule if no suitable room is found
                room = random.choice(suitable_rooms)
                time_slot = random.choice(time_slots)
                schedule_date = start_date + timedelta(days=random.randint(0, 60))
                try:
                    CourseSchedule.objects.create(
                        course=course,
                        room=room,
                        time_slot=time_slot,
                        start_date=schedule_date,
                        end_date=schedule_date + timedelta(days=random.randint(1, 14)),
                        days_of_week=",".join(str(x) for x in random.sample(range(7), 3)),
                        status=random.choice(['SCHEDULED', 'CANCELLED', 'COMPLETED'])
                    )
                except ValidationError as e:
                    print(f"Validation error when creating schedule for course {course.title}: {e}")
                    continue

    @staticmethod
    def create_bookings(users, courses):
        for user in users[:20]:  # Only clients make bookings
            available_courses = list(courses)
            for _ in range(4):  # Try to make 4 bookings for each user
                if not available_courses:
                    break
                course = random.choice(available_courses)
                available_courses.remove(course)
                schedule = course.schedules.filter(status='SCHEDULED').first()
                if schedule and course.available_seats() > 0:
                    Booking.objects.create(
                        user=user,
                        course_schedule=schedule
                    )
                    CourseApplication.objects.create(
                        user=user,
                        course=course,
                        status='approved'
                    )

    def print_summary(self):
        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created {CustomUser.objects.count()} users'))
        self.stdout.write(self.style.SUCCESS(f'Created {Client.objects.count()} clients'))
        self.stdout.write(self.style.SUCCESS(f'Created {Course.objects.count()} courses'))
        self.stdout.write(self.style.SUCCESS(f'Created {CourseSchedule.objects.count()} course schedules'))
        self.stdout.write(self.style.SUCCESS(f'Created {Room.objects.count()} rooms'))
        self.stdout.write(self.style.SUCCESS(f'Created {TimeSlot.objects.count()} time slots'))
        self.stdout.write(self.style.SUCCESS(f'Created {CourseApplication.objects.count()} course applications'))
        self.stdout.write(self.style.SUCCESS(f'Created {Booking.objects.count()} bookings'))

