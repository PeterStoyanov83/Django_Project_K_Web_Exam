from django.test import TestCase
from django.urls import reverse
from client_management.models import CustomUser


class AuthenticationTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password123", email="test@example.com"
        )

    def test_register_view_get(self):
        response = self.client.get(reverse("client_management:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "client_management/register.html")

    def test_register_view_post_valid(self):
        post_data = {
            "username": "newuser",
            "password1": "StrongPassword!123",
            "password2": "StrongPassword!123",
            "email": "newuser@example.com",
            "user_type": "PRIVATE",  # Adding required user_type
        }
        response = self.client.post(reverse("client_management:register"), data=post_data)

        # Debugging for context errors
        if response.context:
            print("Form Errors:", response.context["form"].errors)

        # Asserts
        self.assertEqual(response.status_code, 302)  # Expect redirect
        self.assertRedirects(response, reverse("client_management:profile"))
        self.assertTrue(CustomUser.objects.filter(username="newuser").exists())

    def test_register_view_post_invalid(self):
        post_data = {
            "username": "",  # Invalid username
            "password1": "password12345",
            "password2": "password12345",
            "email": "invalid-email",  # Invalid email format
        }
        response = self.client.post(reverse("client_management:register"), data=post_data)

        # Check that the form is invalid
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required")
        self.assertContains(response, "Enter a valid email address")

        # Ensure no user is created
        self.assertFalse(CustomUser.objects.filter(email="invalid-email").exists())

    def test_login_view_get(self):
        response = self.client.get(reverse("client_management:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "client_management/login.html")

    def test_login_view_post_valid(self):
        post_data = {
            "username": "testuser",
            "password": "password123",
        }
        response = self.client.post(reverse("client_management:login"), data=post_data)

        # Check redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("client_management:profile"))

        # Check session login
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_login_view_post_invalid(self):
        post_data = {
            "username": "wronguser",
            "password": "wrongpassword",
        }
        response = self.client.post(reverse("client_management:login"), data=post_data)

        # Form should remain on the login page with errors
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "")
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_logout_view(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("client_management:logout"))

        # Check redirection
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("client_management:login"))

        # Ensure user is logged out
        self.assertFalse("_auth_user_id" in self.client.session)
