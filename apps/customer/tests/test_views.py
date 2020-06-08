from django import test
from django.contrib.auth import get_user_model
import json
from django.test import Client, RequestFactory
from django.urls import reverse

from ..forms import SignupForm
from ..views import SIGNUP_PAGE_MESSAGE


class SignupTests(test.TestCase):

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_get_request_using_url(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')
        # self.assertIn('form', response.context, msg="form is not in SignupView Context")
        # self.assertIsInstance(response.context['form'], SignupForm)
        # self.assertIn('form_title', response.context)
        # self.assertEqual(response.context['form_title'], SIGNUP_PAGE_MESSAGE)

    def test_get_request_using_url_name(self):
        response = self.client.get(reverse('account_signup'))
        # print("Path:", response.path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')
        self.assertTrue(isinstance(response.context['form'], SignupForm))
        self.assertFormError(response, 'form', None, [])
        # self.ass

    def test_post_request_form_valid_data(self):
        signup_form_data = {
            'first_name': 'Akshay',
            'last_name': 'Satpute',
            'gender': 'male',
            'address': 'satpute male',
            'locality': 'waddi',
            'state': 'Maharashtra',
            'district': 'Sangli',
            'city': 'Miraj',
            'pincode': '416410',
            'phone_number': '7878457845',
            'email': 'akshay@gmail.com',
            'password1': 'satputeps',
            'password2': 'satputeps'
        }

        # form = SignupForm({
        #     'first_name': 'Akshay',
        #     'last_name': 'Satpute',
        #     'gender': 'male',
        #     'address': 'satpute male',
        #     'locality': 'waddi',
        #     'state': 'Maharashtra',
        #     'district': 'Sangli',
        #     'city': 'Miraj',
        #     'pincode': '416410',
        #     'phone_number': '7878457845',
        #     'email_id': 'akshay@gmail.com',
        #     'password': 'satputeps'
        # })
        # json_data = json.dumps(sign_up_form_data)
        form = SignupForm(signup_form_data)
        print("\n\nForm Valid:", form.is_valid())
        response = self.client.post(reverse('account_signup'),  # by default sends data in 'multipart/form-data; '
                                    data=signup_form_data,  # json data
                                    # content_type='application/json',
                                    # for ajax request
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        # print("Request was ajax:", response.is_ajax())

        self.assertEqual(response['content-type'], 'application/json')

        print("\nResponse Status Code:", response.status_code)
        self.assertEqual(response.status_code, 200)

        print("\nResponse Content(String representation) :", response.content)
        # self.assertFormError(response, 'form', None, [])

        print("\n Response Json: ", response.json())
        self.assertTrue(response.json())

        print("\n Response Json Location:", response.json()['location'])
        self.assertEqual(response.json()['location'], reverse('account_login'))

        print("\n Response Json Form:", response.json()['form'])
        self.assertTrue(response.json()['form'])

        print("\n Response HTML Form:", response.json()['html'])
        self.assertFalse(response.json()['html'])

        self.assertTrue(get_user_model().objects.get(email='akshay@gmail.com'))
        # self.assertEqual(request.)
        # form.signup(customer_final=get_user_model())

    def test_post_request_form_invalid_email(self):
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
            'email': 'akshay@.com',
            'password1': 'satputeps',
            'password2': 'satputeps'
        }

        response = self.client.post(reverse('account_signup'),
                                    data=signup_form_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        print("Status code:", response.status_code)
        self.assertEqual(response.status_code, 400)

        print("Response Json Form:", response.json()['form'])
        self.assertTrue(response.json()['form'])

        form = SignupForm(signup_form_data)
        print("Form Errors:", form.errors)
        self.assertFormError(response, 'form', 'email', ['Enter a valid email address.', ])

        self.assertTemplateUsed(response, 'account/signup.html')

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
