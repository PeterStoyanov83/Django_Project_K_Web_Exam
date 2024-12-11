
from django.test import TestCase
from django.urls import reverse
from client_management.models import CustomUser
from course_management.models import Course
from django.core import mail


class PagesViewsTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password123')

    def test_home_view(self):
        lecturer = CustomUser.objects.create_user(username='lecturer', password='password123')

        Course.objects.create(title='Course 1', description='Test Course 1', lecturer=lecturer)

        response = self.client.get(reverse('pages:home'))

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
        response = self.client.get(reverse('pages:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/contact.html')
        self.assertContains(response, 'Contact Us')

    def test_contact_view_post_success(self):
        post_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'This is a test message.',
        }
        response = self.client.post(reverse('pages:contact'), data=post_data)

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
        post_data = {
            'name': '',
            'email': 'invalid-email',
            'message': '',
        }
        response = self.client.post(reverse('pages:contact'), data=post_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pages:contact'))

        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertIn("Please fill in all fields.", str(messages[0]))
        self.assertEqual(len(mail.outbox), 0)

    def test_login_required_view(self):
        response = self.client.get(reverse('pages:restricted_view'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('client_management:login'), response.url)

        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('pages:restricted_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '403.html')