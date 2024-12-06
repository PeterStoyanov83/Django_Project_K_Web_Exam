from django.test import TestCase
from django.urls import reverse
from client_management.models import CustomUser

class ProfileEditViewTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123", email="test@example.com"
        )
        self.client.login(username="testuser", password="password123")

    def test_profile_edit_view_get(self):
        response = self.client.get(reverse('client_management:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client_management/profile_edit.html')

    def test_profile_edit_view_post(self):
        post_data = {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'first_name': 'Updated',
            'last_name': 'User',
            'user_type': 'PRIVATE',  # Include the required user_type field
        }
        response = self.client.post(reverse('client_management:profile_edit'), data=post_data)
        self.user.refresh_from_db()

        # Verify response and updated data
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertEqual(self.user.username, 'updateduser')  # Username should update
