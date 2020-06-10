import datetime
import warnings

from allauth.socialaccount import providers
from allauth.socialaccount.providers.google.provider import GoogleProvider
from allauth.socialaccount.tests import OAuth2TestsMixin
from allauth.tests import MockedResponse
from django import test
from oscar.core.compat import get_user_model
from django.test import Client, RequestFactory
from django.urls import reverse
from .. import validators
from apps.customer.forms.account_forms import SignupForm, BIRTHDAY_FORMAT
from apps.customer.forms.socialaccount_forms import SignupForm as SocialAccountSignupForm
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

    def test_ajax_post_fields_empty(self):
        form = SignupForm({})
        self.assertFalse(form.is_valid())
        response = self.client.post(reverse('account_signup'),
                                    data={},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertIn('form', data)
        context_form = 'form'

        required_fields = [field_name for field_name, field in form.fields.items() if field.required]
        # required_fields = [field_name for field_name, field in form.fields.items() if getattr(field, 'required', False)]
        for field_name in required_fields:
            variable_name = '%s_REQUIRED_ERROR' % field_name.upper()
            if hasattr(validators, variable_name):
                self.assertFormError(response, context_form, field_name, [getattr(validators, variable_name)])

        [self.assertFormError(response, context_form, field, []) for field in form.fields.keys() if
         field not in required_fields]

        # self.assertFormError(response, context_form, 'first_name', [validators.FIRST_NAME_REQUIRED_ERROR])
        # self.assertFormError(response, context_form, 'last_name', [validators.LAST_NAME_REQUIRED_ERROR])
        # self.assertFormError(response, context_form, 'gender', [])
        # self.assertFormError(response, context_form, 'birthday', [])
        # self.assertFormError(response, context_form, 'email', [validators.EMAIL_REQUIRED_ERROR])
        # self.assertFormError(response, context_form, 'password1', [validators.PASSWORD1_REQUIRED_ERROR])
        # self.assertFormError(response, context_form, 'password2', [validators.PASSWORD2_REQUIRED_ERROR])

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

    def test_ajax_post_invalid_email_domain(self):
        signup_form_data = {
            'first_name': 'Akshay',
            'last_name': 'Satpute',
            'phone_number': '7878457845',
            'email': 'akshay@codebread.com',
            'password1': 'satputeps',
            'password2': 'satputeps'
        }
        response = self.client.post(reverse('account_signup'),
                                    data=signup_form_data,
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertTemplateUsed(response, "account/signup.html")
        data = response.json()
        self.assertIn('form', data)
        self.assertIn('html', data)
        form = SignupForm(signup_form_data)
        print("Form Errors:", form.errors)
        self.assertFormError(response, 'form', 'email', [validators.EMAIL_INVALID_DOMAIN_ERROR])

    def test_ajax_post_passwords_must_match(self):
        signup_form_data = {
            'first_name': 'Akshay',
            'last_name': 'Satpute',
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
        self.assertFormError(response, 'form', 'password2', [validators.PASSWORD_NOT_SAME_ERROR])


class SocialAccountSignupViewTests(OAuth2TestsMixin, test.TestCase):
    def setUp(self):
        self.client = Client()
        self.provider_id = GoogleProvider.id
        self.provider = providers.registry.by_id(self.provider_id)

    def get_mocked_response(self,
                            family_name='Penners',
                            given_name='Raymond',
                            name='Raymond Penners',
                            email="raymond.penners@example.com",
                            verified_email=True):
        return MockedResponse(200, """
                 {"family_name": "%s", "name": "%s",
                  "picture": "https://lh5.googleusercontent.com/photo.jpg",
                  "locale": "nl", "gender": "male",
                  "email": "%s",
                  "link": "https://plus.google.com/108204268033311374519",
                  "given_name": "%s", "id": "108204268033311374519",
                  "verified_email": %s }
           """ % (family_name,
                  name,
                  email,
                  given_name,
                  (repr(verified_email).lower())))

    # -------------------------------TO DO---------------------------------------------------------------------
    # def test_get_view_form(self):
    #     resp_mocks = self.get_mocked_response()
    #     if resp_mocks is None:
    #         warnings.warn("Cannot test google provider %s, no oauth mock"
    #                       % self.provider.id)
    #         return
    # resp = self.login(resp_mocks)
    # response = self.client.get(reverse('socialaccount_signup'))
    # response_form = response.context['form']
    # self.assertTrue(isinstance(response_form, SocialAccountSignupForm))
    # sociallogin = response.context['form']
