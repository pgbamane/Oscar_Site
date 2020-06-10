import datetime
from django import test
from oscar.core.compat import get_user_model
from django.test import Client, RequestFactory
from django.urls import reverse

from .. import validators
from ..forms import SignupForm, ProfileForm, BIRTHDAY_FORMAT
from ..views import SIGNUP_PAGE_MESSAGE
from apps.users.models import FEMALE, MALE
import json

User = get_user_model()


class SignupTests(test.TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_get_request_using_url(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_get_request_using_url_name(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)

    def test_view_template_used(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_view_signup_form_instance(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context, msg="form is not in Template Context")
        self.assertIsInstance(response.context['form'], SignupForm, msg="Form is not instance of SignupForm")

    def test_get_request_form_title(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form_title', response.context)
        self.assertEqual(response.context['form_title'], SIGNUP_PAGE_MESSAGE)

    def test_get_request_form_gender_initial_female(self):
        response = self.client.get(reverse('account_signup'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial['gender'], FEMALE)

    def test_ajax_post_valid_data(self):
        signup_form_data = {
            'first_name': 'Akshay',
            'last_name': 'Satpute',
            'gender': MALE,
            'birthday': datetime.date(2000, 1, 30).strftime(BIRTHDAY_FORMAT),
            'phone_number': '7878457845',
            'email': 'akshay@gmail.com',
            'password1': 'satputeps',
            'password2': 'satputeps'
        }
        form = SignupForm(signup_form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('account_signup'),  # by default sends data in 'multipart/form-data; '
                                    data=signup_form_data,
                                    # json data
                                    # content_type='application/json',
                                    # for ajax request
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'application/json')
        # print("\nResponse Content(String representation) :", response.content)
        # data = response.json() both data gettting ways are same
        data = json.loads(response.content.decode('utf8'))

        print("\n Response Json: ", response.json())
        self.assertTrue(data)
        self.assertIn('location', data)
        self.assertEqual(data['location'], reverse('account_login'))
        self.assertIn('form', data)
        print("\n Response HTML Form:", data['html'])
        self.assertFalse(data['html'])
        user = User.objects.get(email=form.cleaned_data['email'])
        #     check whether this user can login
        self.client.login(email=user.email, password=user.password)

    def test_ajax_post_invalid_email(self):
        signup_form_data = {
            'first_name': 'Akshay',
            'last_name': 'Satpute',
            'gender': MALE,
            'birthday': datetime.date(2000, 1, 30).strftime(BIRTHDAY_FORMAT),
            'phone_number': '7878457845',
            'email': 'akshay@.com',
            'password1': 'satputeps',
            'password2': 'satputeps'
        }
        response = self.client.post(reverse('account_signup'),
                                    data=signup_form_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        print("Status code:", response.status_code)
        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'account/signup.html')
        # data = json.loads(response.content.decode('utf8'))
        data = response.json()
        self.assertTrue(data['form'])
        form = SignupForm(signup_form_data)
        print("Form Errors:", form.errors)
        self.assertFormError(response, 'form', 'email', [validators.EMAIL_INVALID_ERROR])

    def test_post_request_form_invalid_email_domain(self):
        signup_form_data = {
            'first_name': 'Akshay',
            'last_name': 'Satpute',
            'gender': 'male',
            'address': 'satpute mala',
            'locality': 'waddi',
            'state': 'Maharashtra',
            'district': 'Sangli',
            'city': 'Miraj',
            'pincode': '416410',
            'phone_number': '7878457845',
            'email': 'akshay@codebread.com',
            'password1': 'satputeps',
            'password2': 'satputeps'
        }
        response = self.client.post(reverse('account_signup'),
                                    data=signup_form_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertTemplateUsed(response, "account/signup.html")

        self.assertTrue(response.json()['form'])

        self.assertTrue(response.json()['html'])

        form = SignupForm(signup_form_data)
        print("Form Errors:", form.errors)
        self.assertFormError(response, 'form', 'email',
                             ['Enter an email address with a valid domain(Gmail, Yahoo, Only)'])

    def test_post_request_form_passwords_must_match(self):
        signup_form_data = {
            'first_name': 'Akshay',
            'last_name': 'Satpute',
            'gender': 'male',
            'address': 'satpute mala',
            'locality': 'waddi',
            'state': 'Maharashtra',
            'district': 'Sangli',
            'city': 'Miraj',
            'pincode': '416410',
            'phone_number': '7878457845',
            'email': 'akshay@gmail.com',
            'password1': 'satputdnc',
            'password2': 'satputeps'
        }

        response = self.client.post(reverse('account_signup'),
                                    data=signup_form_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # content_type=MULTIPART_CONTENT , the values in data will be transmitted with a content type of multipart/form-data.

        self.assertEqual(response.status_code, 400)

        print("Response Content Type :", response['content-type'])
        self.assertEqual(response['content-type'], 'application/json')

        form = SignupForm(signup_form_data)
        print("Form errors : ", form.errors)
        self.assertFormError(response, 'form', 'password2', 'You must type the same password each time.')
