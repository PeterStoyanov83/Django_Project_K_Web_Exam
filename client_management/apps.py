from django.apps import AppConfig
from django.db.models.signals import post_migrate
from datetime import datetime, timedelta


class ClientManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'client_management'

    @staticmethod
    def create_default_data(sender, **kwargs):
        """Create default users, laptops, lecturers, courses, rooms, time slots, and schedules after migrations."""
        from client_management.models import CustomUser, Laptop
        from course_management.models import Lecturer, Course, Room, TimeSlot, CourseSchedule

        # Create Default Users
        if not CustomUser.objects.filter(username='admin').exists():
            CustomUser.objects.create_superuser(
                username='admin',
                email='admin@admin.ad',
                password='admin123'
            )
        if not CustomUser.objects.filter(username='peter').exists():
            CustomUser.objects.create_user(
                username='peter',
                email='peterstoyanov83@gmail.com',
                password='peterko123',
            )
        if not CustomUser.objects.filter(username='normaluser').exists():
            CustomUser.objects.create_user(
                username='normaluser',
                email='normie@user.com',
                password='normie23',
            )

        # Create Default Laptops
        laptops_data = [
            {"brand": "Dell", "model": "XPS 13", "serial_number": "DELL12345",
             "purchase_date": datetime.now().date(),
             "warranty_end_date": datetime.now().date() + timedelta(days=365)},
            {"brand": "Apple", "model": "MacBook Pro", "serial_number": "APPLE12345",
             "purchase_date": datetime.now().date(),
             "warranty_end_date": datetime.now().date() + timedelta(days=365)},
            {"brand": "Lenovo", "model": "ThinkPad X1", "serial_number": "LENOVO12345",
             "purchase_date": datetime.now().date(),
             "warranty_end_date": datetime.now().date() + timedelta(days=365)},
            {"brand": "HP", "model": "Spectre x360", "serial_number": "HP12345",
             "purchase_date": datetime.now().date(),
             "warranty_end_date": datetime.now().date() + timedelta(days=365)},
            {"brand": "Asus", "model": "ZenBook 14", "serial_number": "ASUS12345",
             "purchase_date": datetime.now().date(),
             "warranty_end_date": datetime.now().date() + timedelta(days=365)},
        ]

        for laptop_data in laptops_data:
            Laptop.objects.get_or_create(
                serial_number=laptop_data["serial_number"],
                defaults={
                    "brand": laptop_data["brand"],
                    "model": laptop_data["model"],
                    "purchase_date": laptop_data["purchase_date"],
                    "warranty_end_date": laptop_data["warranty_end_date"],
                }
            )

        # Create Default Lecturers
        lecturer_data = [
            {"name": "Dr. Alexander Dimitrov", "bio": "Expert in AI and machine learning."},
            {"name": "Prof. Elitsa Ivanova", "bio": "Specializes in data science and big data."},
            {"name": "Dr. Nikolay Petrov", "bio": "Advanced Python programming expert."},
            {"name": "Assoc. Prof. Maria Stoyanova", "bio": "Experienced in Django development."},
            {"name": "Dr. Dimitar Yankov", "bio": "Cybersecurity and blockchain specialist."},
            {"name": "Dr. Viktoria Stefanova", "bio": "Focused on machine learning and NLP."},
            {"name": "Prof. Ivan Georgiev", "bio": "Veteran in cloud computing."},
            {"name": "Dr. Pavlina Krumova", "bio": "Algorithms and data structures expert."},
            {"name": "Assoc. Prof. Emil Petrov", "bio": "Agile methodologies expert."},
            {"name": "Dr. Ralitsa Mihaylova", "bio": "Focused on blockchain technologies."},
        ]
        lecturer_objects = []
        for lecturer in lecturer_data:
            lecturer_obj, created = Lecturer.objects.get_or_create(
                name=lecturer["name"], defaults={"bio": lecturer["bio"]}
            )
            lecturer_objects.append(lecturer_obj)

        # Create Default Courses
        course_data = [
            {"title": "Artificial Intelligence Fundamentals",
             "description": "An introduction to AI principles, machine learning techniques, and neural networks.",
             "lecturer": lecturer_objects[0]},
            {"title": "Data Science and Visualization",
             "description": "A practical course on data analysis and visualization techniques.",
             "lecturer": lecturer_objects[1]},
            {"title": "Advanced Python Programming",
             "description": "A deep dive into Python, including advanced algorithms and optimization techniques.",
             "lecturer": lecturer_objects[2]},
            {"title": "Web Development with Django",
             "description": "Comprehensive coverage of Django for building scalable web applications.",
             "lecturer": lecturer_objects[3]},
            {"title": "Introduction to Cybersecurity",
             "description": "Basics of cybersecurity, including threat detection, prevention, and risk assessment.",
             "lecturer": lecturer_objects[4]},
            {"title": "Cloud Computing Essentials",
             "description": "Learn about cloud services, deployment, and security.",
             "lecturer": lecturer_objects[6]},
            {"title": "Big Data Analytics",
             "description": "Explore tools and frameworks for processing and analyzing large datasets.",
             "lecturer": lecturer_objects[2]},
            {"title": "Machine Learning for Beginners",
             "description": "A beginner-friendly course on machine learning algorithms and their applications.",
             "lecturer": lecturer_objects[0]},
            {"title": "Software Project Management",
             "description": "Learn methodologies like Agile and Scrum to manage software projects effectively.",
             "lecturer": lecturer_objects[8]},
            {"title": "Blockchain and Cryptocurrency",
             "description": "Fundamentals of blockchain technology and its use in cryptocurrency.",
             "lecturer": lecturer_objects[9]},
        ]
        course_objects = []
        for course in course_data:
            course_obj, created = Course.objects.get_or_create(
                title=course["title"],
                defaults={"description": course["description"], "lecturer": course["lecturer"]},
            )
            course_objects.append(course_obj)

        # Create Default Rooms
        room_names = ["Room A", "Room B", "Room C", "Room D", "Room E"]
        for room_name in room_names:
            Room.objects.get_or_create(
                name=room_name,
                defaults={"capacity": 30}
            )

    def ready(self):
        super_ready = super().ready()
        post_migrate.connect(self.create_default_data, sender=self)
        return super_ready
