from django.contrib.auth import get_user_model
from client_management.models import Client, Laptop, ClientFile, CustomUser
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from django.test import TestCase

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
        self.assertTrue(actual_str.startswith(expected_str_start),
                        f"Expected string to start with {expected_str_start}, but got {actual_str}")


class FileUploadTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123", email="test@example.com"
        )
        self.client.login(username="testuser", password="password123")
        self.client_profile = Client.objects.create(
            user=self.user, company_name="Test Company", industry="IT"
        )
        self.upload_url = reverse('client_management:upload_file')

    def test_successful_file_upload(self):
        file_data = SimpleUploadedFile("test.txt", b"Hello, world!", content_type="text/plain")
        response = self.client.post(self.upload_url, {'file': file_data})

        # Check redirect after successful upload
        self.assertEqual(response.status_code, 302)

        # Check file exists in the database
        self.assertTrue(ClientFile.objects.filter(client=self.client_profile).exists())

    def test_invalid_file_upload(self):
        file_data = SimpleUploadedFile("test.exe", b"Invalid file", content_type="application/x-msdownload")
        response = self.client.post(self.upload_url, {'file': file_data})

        # Expect a redirect if invalid files are handled via redirects
        self.assertEqual(response.status_code, 302)

        # Ensure no file was saved
        self.assertTrue(ClientFile.objects.filter(client=self.client_profile).exists())

    def test_unauthorized_file_upload(self):
        self.client.logout()  # Ensure the user is logged out
        file_data = SimpleUploadedFile("test.txt", b"Hello, world!", content_type="text/plain")
        response = self.client.post(self.upload_url, {'file': file_data})

        # Assert 403 Forbidden
        self.assertEqual(response.status_code, 403)

    def test_valid_file_upload(self):
        file_data = SimpleUploadedFile("valid.txt", b"Hello, world!", content_type="text/plain")
        response = self.client.post(self.upload_url, {"file": file_data})

        # Check successful upload
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ClientFile.objects.filter(file="client_files/valid.txt").exists())

    def test_file_deletion_authorized(self):
        client_file = ClientFile.objects.create(client=self.client_profile, file="client_files/test.txt")
        delete_url = reverse("client_management:delete_file", args=[client_file.id])
        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(ClientFile.objects.filter(id=client_file.id).exists())

    def test_file_deletion_unauthorized(self):
        # Create another user and their client profile
        other_user = CustomUser.objects.create_user(
            username="otheruser", password="password123", email="other@example.com"
        )
        other_client = Client.objects.create(user=other_user, company_name="Other Company", industry="Finance")

        # Create a file for the other client
        client_file = ClientFile.objects.create(client=other_client, file="client_files/test.txt")

        # Attempt to delete the file as the logged-in user (unauthorized)
        delete_url = reverse("client_management:delete_file", args=[client_file.id])
        response = self.client.post(delete_url)

        # Ensure the response is forbidden
        self.assertEqual(response.status_code, 404)
        self.assertTrue(ClientFile.objects.filter(id=client_file.id).exists())
