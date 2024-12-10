from django.test import TestCase
from client_management.forms import ClientForm

class ClientFormTest(TestCase):
    def test_client_form_valid(self):
        form_data = {'company_name': 'Test Company', 'industry': 'Technology'}
        form = ClientForm(data=form_data)
        self.assertTrue(form.is_valid(), "Form should be valid with correct data.")

    def test_client_form_invalid(self):
        form_data = {'company_name': '', 'industry': 'Technology'}
        form = ClientForm(data=form_data)
        self.assertFalse(form.is_valid(), "Form should be invalid without a company name.")
