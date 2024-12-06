from django.test import TestCase
from django.contrib.auth import get_user_model
from client_management.models import Client, Laptop, ClientFile
from datetime import date

User = get_user_model()

class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@example.com", user_type="BUSINESS")
        self.client = Client.objects.create(user=self.user, company_name="Test Company", industry="Technology")

    def test_client_str(self):
        self.assertEqual(str(self.client), "Test Company")


class LaptopModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.client = Client.objects.create(user=self.user, company_name="Test Company", industry="Technology")
        self.laptop = Laptop.objects.create(
            client=self.client,
            brand="Dell",
            model="XPS",
            serial_number="12345",
            purchase_date=date(2020, 1, 1),
            warranty_end_date=date(2023, 1, 1),
            status="active",
        )

    def test_laptop_str(self):
        self.assertEqual(str(self.laptop), "Dell XPS - 12345")


class ClientFileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.client = Client.objects.create(user=self.user, company_name="Test Company", industry="Technology")
        self.file = ClientFile.objects.create(client=self.client, file="test_file.pdf")

    def test_client_file_str(self):
        expected_str_start = "test_file.pdf - "
        actual_str = str(self.file)
        self.assertTrue(actual_str.startswith(expected_str_start), f"Expected string to start with {expected_str_start}, but got {actual_str}")
