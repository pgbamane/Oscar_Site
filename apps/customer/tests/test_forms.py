from allauth.account.models import EmailAddress
from django.test import TestCase
from oscar.core.compat import get_user_model
from apps.customer.forms.account_forms import SignupForm, ProfileForm, BIRTHDAY_PLACEHOLDER, MINIMUM_BIRTHDAY
from apps.customer.forms.socialaccount_forms import SignupForm as SocialAccount_SignupForm
from allauth.socialaccount.models import SocialLogin, SocialAccount, SocialToken
from apps.users.models import FEMALE, MALE
import datetime
from django.test.client import RequestFactory
from apps.customer import validators
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.models import AnonymousUser

User = get_user_model()


class SignupFormTests(TestCase):
    def setUp(self):
        super(SignupFormTests, self).setUp()
        self.factory = RequestFactory()

    def test_form_fields(self):
        expected_fields = {'first_name',
                           'last_name',
                           'gender',
                           'birthday',
                           'phone_number',
                           'email',
                           'password1',
                           'password2'}
        form = SignupForm()
        # self.fail(form.fields.keys())
        form_fields = set(form.fields.keys())
        self.assertEqual(form_fields, expected_fields)

    def test_form_fields_order(self):
        expected_fields_order = ['first_name',
                                 'last_name',
                                 'gender',
                                 'birthday',
                                 'phone_number',
                                 'email',
                                 'password1',
                                 'password2']

        form = SignupForm()
        fields_order = list(form.fields.keys())
        print("Form Field Order : ", fields_order)
        self.assertEqual(fields_order, expected_fields_order)

    def test_form_valid_data(self):
        form_data = {
            'first_name': 'Akshay',
            'last_name': 'Satpute',
            'gender': MALE,
            'birthday': datetime.date(year=2000, month=1, day=1),
            'phone_number': '7878457845',
            'email': 'akshay@gmail.com',
            'password1': 'satputeps',
            'password2': 'satputeps'
        }
        form = SignupForm(form_data)

        print("\nForm Valid: ", form.is_valid())
        self.assertTrue(form.is_valid())

        print("\nForm errors: {x}".format(x=form.errors if form.errors else "No errors."))
        self.assertEqual(form.errors, {})

        # request = self.factory.post(reverse('account_signup'))
        # form.save(request)
        # user = User.object.get(first_name=form.cleaned_data['first_name'])
        # self.email_address = EmailAddress.objects.create(
        #     user=user,
        #     email=user.email,
        #     verified=True,
        #     primary=True)
        #
        # print("\nFirst Name:", user.first_name)

    def test_form_first_name_required_error(self):
        form = SignupForm({
            'first_name': '',
        })
        print("\nForm Valid: ", form.is_valid())
        print("First Name empty: {x}".format(x="empty" if not form.data['first_name'] else 'Not empty'))
        print("First name required error: ", form.errors['first_name'])
        self.assertEqual(form.errors['first_name'], [validators.FIRST_NAME_REQUIRED_ERROR])

    def test_form_last_name_required_error(self):
        form = SignupForm({
            'last_name': '',
        })
        print("Form Valid: ", form.is_valid())
        self.assertFalse(form.is_valid())
        print("Last Name empty: {x}".format(x="empty" if not form.data['last_name'] else 'Not empty'))
        print("Last Name required error: ", form.errors['last_name'])
        self.assertEqual(form.errors['last_name'], [validators.LAST_NAME_REQUIRED_ERROR])

    def test_form_gender_default_female(self):
        form = SignupForm()
        print("Form valid: ", form.is_valid())
        self.assertFalse(form.is_bound)
        print('Gender Initial Value: ', form.initial['gender'])
        self.assertEqual(form.initial['gender'], FEMALE)

    def test_form_birthday_placeholder(self):
        form = SignupForm()
        print("Form Birthday placeholder: ", form.fields['birthday'].widget.attrs['placeholder'])
        self.assertEqual(form.fields['birthday'].widget.attrs['placeholder'], BIRTHDAY_PLACEHOLDER)

    def test_form_birthday_format(self):
        form = SignupForm({
            'birthday': datetime.date(1995, 7, 23)
        })
        self.assertFalse(form.is_valid())
        # self.assertEqual(form.errors['birthday'], [validators.DATE_INCORRECT_FORMAT_ERROR])

    def test_form_birthday_date_fields(self):
        year = 1995
        month = 7
        day = 23
        form = SignupForm({
            'birthday': datetime.date(year=year, month=month, day=day)
        })
        print("Form Bound: ", form.is_bound)
        self.assertFalse(form.is_valid())
        # self.assertEqual(form.fields['birthday'].input_formats[0], BIRTHDAY_FORMAT)
        self.assertEqual(form.cleaned_data['birthday'].year, year)
        self.assertEqual(form.cleaned_data['birthday'].month, month)
        self.assertEqual(form.cleaned_data['birthday'].day, day)

    def test_form_birthday_greater_than_today_invalid(self):
        form = SignupForm({
            'birthday': datetime.date.today() + datetime.timedelta(days=1)
        })
        self.assertFalse(form.is_valid())
        print("Form Birthday Errors : ", form.errors['birthday'])
        self.assertEqual(form.errors['birthday'], [validators.BIRTHDAY_INVALID_ERROR])

    def test_form_birthday_less_than_minimum(self):
        form = SignupForm({
            'birthday': MINIMUM_BIRTHDAY - datetime.timedelta(days=1)
        })
        self.assertFalse(form.is_valid())
        print("Form Birthday Errors : ", form.errors['birthday'])
        self.assertEqual(form.errors['birthday'], [validators.BIRTHDAY_INVALID_ERROR])

    def test_form_email_required_error(self):
        form = SignupForm({})
        self.assertFalse(form.is_valid())
        print("Form Email Required error: ", form.errors['email'])
        self.assertEqual(form.errors['email'], [validators.EMAIL_REQUIRED_ERROR])

    def test_form_email_valid_domain(self):
        form = SignupForm({
            'email': 'pradnya@facebook.com'
        })
        self.assertFalse(form.is_valid())
        print("Form email errors: ", form.errors['email'])
        self.assertEqual(form.errors['email'], [validators.EMAIL_INVALID_DOMAIN_ERROR])

    def test_form_email_already_taken(self):
        User.objects.create_user(first_name="Pradnya",
                                 last_name="Bamane",
                                 email="pradnya@gmail.com",
                                 password="satputeps")
        pradnya_user = User.objects.get(first_name='Pradnya')
        self.assertTrue(pradnya_user)
        self.assertEqual(pradnya_user.first_name, "Pradnya")
        self.assertEqual(pradnya_user.last_name, "Bamane")
        self.assertEqual(pradnya_user.email, "pradnya@gmail.com")
        form_data = {
            'first_name': 'Pradnya',
            'email': 'pradnya@gmail.com',
            'password1': 'satputeps',
            'password2': 'satputeps'
        }
        form = SignupForm(form_data)
        self.assertFalse(form.is_valid())
        print("Form email already taken error: ", form.errors['email'])
        self.assertEqual(form.errors['email'], [validators.EMAIL_ALREADY_TAKEN_ERROR])

    def test_form_both_passwords_not_equal_error(self):
        form = SignupForm({
            'password1': 'satputeps',
            'password2': 'satkjkvf'
        })
        self.assertFalse(form.is_valid())
        print("Both passwords: %s , %s" % (form.data['password1'], form.data['password2']))
        self.assertEqual(form.errors['password2'], [validators.PASSWORD_NOT_SAME_ERROR])


class ProfileFormMetaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\n Creating User: in setUpTestData() method")
        super(ProfileFormMetaTests, cls).setUpTestData()
        # cls.user = get_user_model().objects.create_user(first_name="Akshay",
        #                                                 last_name="Satpute",
        #                                                 email='akshay@gmail.com')
        cls.profile_form_class = ProfileForm
        # cls.profile_form = ProfileForm(user=cls.user)

    def test_form_fields(self):
        """
        check the profile form contains all the fields
        :return:
        """
        fields = self.profile_form_class._meta.fields
        fields_list = ['first_name', 'last_name', 'gender', 'birthday', 'email', 'phone_number']
        print(fields)
        self.assertTrue(set(fields) == set(fields_list))

    def test_form_email_required(self):
        """
        test whether email has required True
        :return:
        """
        email_required = self.profile_form_class.base_fields.get('email').required
        print("Email Required:", email_required)
        self.assertIs(email_required, True)

    def test_form_phone_number_not_required(self):
        """
        test whether phone number is not required
        :return:
        """
        phone_required = self.profile_form_class.declared_fields.get('phone_number').required
        print("Phone required:", phone_required)
        self.assertIs(phone_required, False)

    def test_form_first_name_required(self):
        """
        test whether first_name required
        :return:
        """
        first_name_required = self.profile_form_class.base_fields.get('first_name').required
        print("First Name required: ", first_name_required)
        self.assertIs(first_name_required, True)


# test_profile_form_fields = ProfileFormTestCase('test_profile_form_fields')

class ProfileFormDataTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("Creating User and Profile form...")
        super(ProfileFormDataTests, cls).setUpTestData()
        cls.user = User.objects.create_user(first_name="Pradnya",
                                            last_name="Bamane",
                                            email='pradnya23@gmail.com')
        cls.profile_form = ProfileForm(user=cls.user)
        # cls.client = Client()

    def setUp(self):
        self.user.refresh_from_db()
        self.profile_form = ProfileForm(user=self.user)

    # def test_form_takes_user_model_fields(self):
    #     self.assertTrue(self.profile_form.is_valid())
    #     print("Form errors:", self.profile_form.errors)

    def test_form_fields_order(self):
        expected_fields_order = [
            'first_name',
            'last_name',
            'gender',
            'birthday',
            'phone_number',
            'email'
        ]
        fields = self.profile_form.fields.keys()
        print("Form fields:", self.profile_form.fields.keys())
        self.assertEqual(list(fields), expected_fields_order)

    def test_form_first_name_required(self):
        first_name_required = self.profile_form.fields['first_name'].required
        print("\n First name required:", first_name_required)
        self.assertTrue(first_name_required)

    def test_form_first_name_required_error(self):
        form = ProfileForm(user=self.user, data={'first_name': ''})
        # first_name_required_error = self.profile_form.fields['first_name'].error_messages['required']
        self.assertFalse(form.is_valid())
        self.assertEqual(form.data['first_name'], '')
        print('First Name required error: ', form.errors['first_name'])
        self.assertEqual(form.errors['first_name'], [validators.FIRST_NAME_REQUIRED_ERROR])

    def test_form_last_name_not_required(self):
        last_name_required = self.profile_form.fields['last_name'].required
        print("\n Last name required:", last_name_required)
        self.assertFalse(last_name_required)

    def test_form_gender_initial_female(self):
        gender_initial = self.profile_form.fields['gender'].initial
        print("Gender Initial:", gender_initial)
        self.assertEqual(gender_initial, 'female')

    def test_form_birthday_placeholder(self):
        birthday_placeholder = self.profile_form.fields['birthday'].widget.attrs['placeholder']
        print("Birthday placeholder:", birthday_placeholder)
        self.assertEqual(birthday_placeholder, 'Select Date of Birth')

    def test_form_birthday_format(self):
        options_birthday_format = self.profile_form.fields['birthday'].widget.options_param['format']
        widget_format = self.profile_form.fields['birthday'].widget.format
        print("Birthday Format:", options_birthday_format, "\n Widget format:", widget_format)
        self.assertEqual(options_birthday_format, "DD/MM/YYYY")
        self.assertEqual(widget_format, "%d/%m/%Y")

    def test_form_phone_number_required(self):
        phone_required = self.profile_form.fields['phone_number'].required
        print("Phone number required:", phone_required)
        self.assertIs(phone_required, False)

    def test_form_email_required(self):
        email_required = self.profile_form.fields['email'].required
        print('Email required:', email_required)
        self.assertIs(email_required, True)

    # don't test django default functionalities, it is already tested
    # def test_form_email_default_required_error(self):
    #     email_required_error = self.profile_form.fields['email']
    #     print('Email Required error:', email_required_error)
    #

    # test crispy form css id and signup button id

    def test_form_email_required_error(self):
        form = ProfileForm(user=self.user, data={'email': ''})
        self.assertFalse(form.is_valid())
        # even str=' ' single space is not empty string, check it
        is_empty = not (form.data['email'] and not form.data['email'].isspace())
        print("Email empty:", is_empty)
        print("Email Required Error:", form.errors['email'])
        self.assertEqual(form.errors['email'], [validators.EMAIL_REQUIRED_ERROR])

    def test_form_email_invalid_error(self):
        form = ProfileForm(user=self.user, data={'email': 'prad@.com'})
        self.assertFalse(form.is_valid())
        print("Email: ", form.data['email'])
        self.assertEqual(form.errors['email'],
                         ['Enter a valid email address.'])


class SocialAccountSignupFormTests(TestCase):
    def setUp(self):
        super(SocialAccountSignupFormTests, self).setUp()

    @classmethod
    def setUpTestData(cls):
        cls.sociallogin = SocialLogin(
            user=User(email="verified@gmail.com"),
            account=SocialAccount(
                provider='google'
            ),
            email_addresses=[
                EmailAddress(
                    email="verified@gmail.com",
                    verified=True,
                    primary=True
                )
            ]
        )
        cls.form = SocialAccount_SignupForm(sociallogin=cls.sociallogin, data={'email': "verified@gmail.com"})

    def test_form_fields(self):
        # form = SocialAccount_SignupForm()
        self.assertIn('email', self.form.fields)

    def test_form_field_values(self):
        self.assertEqual(self.form['email'].value(), "verified@gmail.com")
        # self.assertTrue(form.fields)

    def test_social_user_account_token_emailaddress_created(self):
        factory = RequestFactory()
        request = factory.post('/accounts/social/signup/')
        request.user = AnonymousUser()
        SessionMiddleware().process_request(request)
        MessageMiddleware().process_request(request)

        self.assertTrue(self.form.is_valid())
        self.form.save(request)
        # sociallogin = SocialLogin.(email=self.form['email'].value())
        user = get_user_model().objects.get(id=self.form.sociallogin.user.id)
        socialaccount = SocialAccount.objects.get(user=self.form.sociallogin.user)
        self.assertFalse(SocialToken.objects.filter(account=socialaccount, token=self.form.sociallogin.token))
        self.assertTrue(EmailAddress.objects.get_for_user(user=user, email=user.email))
