from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser, Client as ClientModel, Laptop, ClientFile
from .forms import CustomUserForm, ClientForm, ClientFileForm

User = get_user_model()

class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = ClientModel.objects.create(
            user=self.user,
            company_name='Test Company',
            industry='Test Industry'
        )

    def test_client_creation(self):
        self.assertTrue(isinstance(self.client, ClientModel))
        self.assertEqual(self.client.__str__(), self.client.company_name)

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='12345'
        )

    def test_custom_user_creation(self):
        self.assertTrue(isinstance(self.user, CustomUser))
        self.assertEqual(self.user.__str__(), self.user.username)

class ClientFormTest(TestCase):
    def test_client_form_valid_data(self):
        form = ClientForm(data={
            'company_name': 'New Company',
            'industry': 'New Industry'
        })
        self.assertTrue(form.is_valid())

    def test_client_form_invalid_data(self):
        form = ClientForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

class ClientManagementViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client_model = ClientModel.objects.create(
            user=self.user,
            company_name='Test Company',
            industry='Test Industry'
        )

    def test_profile_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('client_management:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client_management/profile.html')

    def test_profile_edit_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('client_management:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client_management/profile_edit.html')

class ClientManagementIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_client_registration_and_profile_update(self):
        # Register a new client
        response = self.client.post(reverse('client_management:register'), data={
            'username': 'newclient',
            'email': 'newclient@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration

        # Login with the new client
        self.client.login(username='newclient', password='testpassword123')

        # Update profile
        response = self.client.post(reverse('client_management:profile_edit'), data={
            'company_name': 'New Company Ltd',
            'industry': 'Technology',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful update

        # Check if the profile was updated
        updated_client = ClientModel.objects.get(user__username='newclient')
        self.assertEqual(updated_client.company_name, 'New Company Ltd')
        self.assertEqual(updated_client.industry, 'Technology')

class LaptopModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = ClientModel.objects.create(
            user=self.user,
            company_name='Test Company',
            industry='Test Industry'
        )
        self.laptop = Laptop.objects.create(
            client=self.client,
            brand='Test Brand',
            model='Test Model',
            serial_number='123456',
            purchase_date='2023-01-01',
            warranty_end_date='2024-01-01',
            status='active'
        )

    def test_laptop_creation(self):
        self.assertTrue(isinstance(self.laptop, Laptop))
        self.assertEqual(str(self.laptop), 'Test Brand Test Model - 123456')

class ClientFileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client = ClientModel.objects.create(
            user=self.user,
            company_name='Test Company',
            industry='Test Industry'
        )
        self.client_file = ClientFile.objects.create(
            client=self.client,
            file='test_file.pdf'
        )

    def test_client_file_creation(self):
        self.assertTrue(isinstance(self.client_file, ClientFile))
        self.assertEqual(str(self.client_file), 'Test Company - test_file.pdf')

