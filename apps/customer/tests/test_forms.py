from django.test import TestCase
from oscar.core.compat import get_user_model
from ..forms import SignupForm, ProfileForm, FIRST_NAME_REQUIRED_ERROR, EMAIL_REQUIRED_ERROR


class SignupFormTestCase(TestCase):
    def test_signup_form_field_errors(self):
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
        form = SignupForm(signup_form_data)

        print("\n\nForm Valid:", form.is_valid())
        self.assertTrue(form.is_valid())

        print("\n\nForm errors:", form.errors)
        self.assertEqual(form.errors, {})

        print("\n first_name:", form.cleaned_data['first_name'])

    def test_form_field_order(self):
        signup_form = SignupForm()

        print("Form Field Order : ", signup_form.field_order)
        self.assertEqual(signup_form.field_order,
                         ['first_name', 'last_name', 'gender', 'address', 'locality', 'state', 'district', 'city',
                          'pincode', 'phone_number', 'email', 'password1', 'password2'])


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
        User = get_user_model()
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
        self.assertEqual(form.errors['first_name'], FIRST_NAME_REQUIRED_ERROR)

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
        self.assertEqual(form.errors['email'], EMAIL_REQUIRED_ERROR)

    def test_form_email_invalid_error(self):
        form = ProfileForm(user=self.user, data={'email': 'prad@.com'})
        self.assertFalse(form.is_valid())
        print("Email: ", form.data['email'])
        self.assertEqual(form.errors['email'],
                         ['Enter a valid email address.'])

# class SampleTestCase(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         print("setUpTestData() called :")
#         cls.name = 'Pradnya'
#
#     def test_first_name(self):
#         self.assertEqual(self.name, 'Pradnya')
#
#     def test_change_name(self):
#         self.name = 'Meenu'
#         self.assertEqual(self.name, 'Meenu')
