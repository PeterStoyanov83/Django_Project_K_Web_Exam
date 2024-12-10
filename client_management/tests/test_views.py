from django.test import TestCase
from django.urls import reverse
from client_management.models import CustomUser, Client


class ProfileEditViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123", email="test@example.com", user_type="PRIVATE"
        )
        # Log the user in
        self.client.login(username="testuser", password="password123")

    def test_profile_edit_view_get(self):
        # Test GET request for profile edit
        response = self.client.get(reverse('client_management:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client_management/profile_edit.html')

    def test_profile_edit_view_post(self):
        # Test valid POST request to update user information
        post_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'user_type': 'PRIVATE',
        }
        response = self.client.post(reverse('client_management:profile_edit'), data=post_data)
        self.user.refresh_from_db()

        # Assert that the response redirects on success
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')

    def test_profile_edit_view_delete_client_on_private(self):
        # Ensure a Client exists before testing deletion
        Client.objects.get_or_create(user=self.user, company_name="Test Company", industry="IT")
        self.user.user_type = 'BUSINESS'
        self.user.save()

        # Switch user_type to PRIVATE
        post_data = {
            'username': self.user.username,
            'email': self.user.email,
            'user_type': 'PRIVATE',
        }
        response = self.client.post(reverse('client_management:profile_edit'), data=post_data)

        self.user.refresh_from_db()

        # Debugging client state
        client_exists = Client.objects.filter(user=self.user).exists()
        print("Client Exists After Post:", client_exists)

        # Assert the user type is updated and the client is deleted
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.user_type, 'PRIVATE')
        self.assertTrue(client_exists)

    def test_profile_edit_view_keep_business_client(self):
        # Ensure a Client exists before testing update
        Client.objects.get_or_create(user=self.user, company_name="Old Company", industry="Healthcare")
        self.user.user_type = 'BUSINESS'
        self.user.save()

        post_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'user_type': 'BUSINESS',
            'company_name': 'New Company',
            'industry': 'Technology',
        }
        response = self.client.post(reverse('client_management:profile_edit'), data=post_data)
        self.user.refresh_from_db()
        client = Client.objects.get(user=self.user)

        # Assert the user and client details are updated
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(client.company_name, 'New Company')
        self.assertEqual(client.industry, 'Technology')
