# pages/tests.py

from django.test import TestCase
from django.urls import reverse
from client_management.models import CustomUser
from course_management.models import Course
from django.core import mail


class PagesViewsTest(TestCase):
    def setUp(self):
        # Create a user for testing login-required views if needed in the future
        self.user = CustomUser.objects.create_user(username='testuser', password='password123')

    def test_home_view(self):
        # Create a lecturer user
        lecturer = CustomUser.objects.create_user(username='lecturer', password='password123')

        # Create some courses for testing the homepage
        Course.objects.create(title='Course 1', description='Test Course 1', lecturer=lecturer)

        response = self.client.get(reverse('pages:home'))

        # Ensure the response status is OK and uses the correct template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/home.html')

        self.assertContains(response, 'Test Course 1')

    def test_about_view(self):
        # Test that the about view renders correctly
        response = self.client.get(reverse('pages:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/about.html')
        self.assertContains(response, 'About Us')

    def test_contact_view_get(self):
        # Test the contact view's GET request
        response = self.client.get(reverse('pages:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/contact.html')
        self.assertContains(response, 'Contact Us')

    def test_contact_view_post_success(self):
        # Test the contact form submission (successful)
        post_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.',
        }
        response = self.client.post(reverse('pages:contact'), data=post_data)

        # Ensure the form redirects on successful email send
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:contact'))

        # Verify that a success message is sent
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your message has been sent successfully. We'll get back to you soon!")

        # Check if an email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('contact form', mail.outbox[0].subject)
        self.assertIn('This is a test message.', mail.outbox[0].body)

    def test_contact_view_post_failure(self):
        # Test the contact form submission (failure case)
        post_data = {
            'name': '',
            'email': 'invalid-email',
            'message': '',
        }
        response = self.client.post(reverse('pages:contact'), data=post_data)

        # Ensure the form redirects on failure
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:contact'))

        # Verify that an error message is sent
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertIn("Please fill in all fields.", str(messages[0]))

        # Ensure no emails are sent
        self.assertEqual(len(mail.outbox), 0)

    def test_login_required_view(self):
        # Test that a login-required view redirects unauthenticated users
        response = self.client.get(reverse('pages:restricted_view'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('client_management:login'), response.url)

        # Log in the user and access the restricted view
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('pages:restricted_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '403.html')