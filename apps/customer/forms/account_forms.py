import datetime
from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, Reset
from django.core.exceptions import ValidationError
from oscar.apps.customer.forms import UserForm
from django import forms
from django.urls import reverse
from oscar.core.compat import (
    existing_user_fields, get_user_model
)
from oscar.core.loading import get_profile_class
from allauth.account.forms import SignupForm as CoreSignUpForm, PasswordField
from django.utils.translation import ugettext_lazy as _
from bootstrap_datepicker_plus import DatePickerInput
from apps.users.models import FEMALE, GENDER_OPTIONS
from apps.customer import validators
from apps.customer.validators import validate_date_format

User = get_user_model()

BIRTHDAY_PLACEHOLDER = 'Select Date of Birth'
BIRTHDAY_FORMAT = "%d-%m-%Y"
MINIMUM_BIRTHDAY = datetime.date(year=1960, month=1, day=1)


class SignupForm(CoreSignUpForm):
    first_name = forms.CharField(max_length=30,
                                 label="First Name",
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Enter First Name',
                                         'autofocus': 'autofocus',
                                     }),
                                 )
    last_name = forms.CharField(max_length=30,
                                label="Last Name",
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Enter Last Name',
                                        'autofocus': 'autofocus',
                                    }),
                                )

    gender = forms.ChoiceField(label="Gender",
                               choices=GENDER_OPTIONS,
                               widget=forms.RadioSelect()
                               )
    birthday = forms.DateField(label='Birthday',
                               input_formats=[BIRTHDAY_FORMAT, ],
                               widget=DatePickerInput(
                                   options={
                                       # display format
                                       'format': BIRTHDAY_FORMAT,
                                       'minDate': datetime.date(year=1960, month=1, day=1).strftime(BIRTHDAY_FORMAT),
                                       'maxDate': datetime.date.today().strftime(BIRTHDAY_FORMAT)
                                   },
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': BIRTHDAY_PLACEHOLDER
                                   }
                               ))
    phone_number = forms.CharField(max_length=13,
                                   label="Phone No.",
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Phone Number',
                                           'autofocus': 'autofocus',
                                       }
                                   ))

    field_order = ['first_name', 'last_name', 'gender', 'birthday',
                   'phone_number', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        # get initial arguments if any
        initial_arguments = kwargs.get('initial', None)
        updated_initial = {}
        updated_initial['gender'] = FEMALE
        # Finally update the kwargs initial reference
        kwargs.update(initial=updated_initial)
        super(SignupForm, self).__init__(*args, **kwargs)
        # self.fields['birthday'].validators.append(validate_date_format
        self.fields['password2'] = PasswordField(label=_("Confirm Password"))
        self.fields['email'] = forms.EmailField(label=_('Email ID'),
                                                widget=forms.EmailInput(
                                                    attrs={
                                                        'class': 'form-control',
                                                        'placeholder': 'Email ID'
                                                    }
                                                ), )
        self.fields['gender'].required = False
        self.fields['birthday'].required = False
        self.fields['phone_number'].required = False
        # self.fields['first_name'].error_messages['required'] = validators.FIRST_NAME_REQUIRED_ERROR
        # non_required_fields = ['gender', 'birthday', 'phone_number']

        required_fields = [field_name for field_name, field in self.fields.items() if field.required]
        for field in self.fields.keys():
            if field in required_fields:
                variable_name = '%s_REQUIRED_ERROR' % field.upper()
                if hasattr(validators, variable_name):
                    self.fields[field].error_messages['required'] = getattr(validators, variable_name)

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        # try:
        #     datetime.datetime.strptime(str(birthday), BIRTHDAY_FORMAT)
        # except ValueError:
        #     raise forms.ValidationError(validators.DATE_INCORRECT_FORMAT_ERROR)
        MAXIMUM_DATE = datetime.date.today()
        if birthday:
            if birthday > MAXIMUM_DATE or birthday < MINIMUM_BIRTHDAY:
                raise forms.ValidationError(validators.BIRTHDAY_INVALID_ERROR)

        return birthday

    def save(self, request):
        print("\nSign Up Form Save Method Called: ")
        # actually saving of user is done by Adapter class
        user = super(SignupForm, self).save(request)
        return user

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = 'id-Sign-Up-Form'
        helper.form_method = 'POST'
        helper.form_action = reverse('account_signup')
        helper.layout = Layout(
            Row(
                Column('first_name', css_class="form-group col-md-6 mb-0"),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            InlineRadios('gender', css_class="form-group"),
            Field('birthday', css_class="form-group col-md-10 mb-0"),
            Field('phone_number', css_class="form-group col-md-10 mb-0"),
            Field('email', css_class="form-group col-md-10 mb-0"),
            Field('password1', css_class="form-group col-md-10 mb-0"),
            Field('password2', css_class="form-group col-md-10 mb-0"),
            Row(
                Submit('submit', 'Sign Up', css_class="form-group btn col-md-offset-1 col-md-2 mb-0",
                       css_id='sign-up-id'),
                Reset('reset', 'Reset', css_class='form-group btn col-md-offset-1 col-md-2 mb-0 btn-danger')
            )
        )
        # helper.attrs('novalidate')
        return helper


class ProfileForm(UserForm):
    first_name = forms.CharField(max_length=30,
                                 required=True,
                                 label="First Name",
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Enter First Name',
                                         'autofocus': 'autofocus',
                                     }))
    last_name = forms.CharField(max_length=30,
                                required=False,
                                label="Last Name",
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Enter Last Name',
                                        'autofocus': 'autofocus',
                                    }
                                ))
    gender = forms.ChoiceField(label="Gender",
                               choices=GENDER_OPTIONS,
                               initial=GENDER_OPTIONS[0][0],
                               widget=forms.RadioSelect(
                                   # attrs={
                                   #     'class': 'form-control',
                                   # },
                                   # choices=GENDER_OPTIONS
                               ))
    birthday = forms.DateField(label='Birthday',
                               required=False,
                               widget=DatePickerInput(
                                   options={
                                       'format': "DD/MM/YYYY",
                                       'minDate': '01/01/1960',
                                   },
                                   attrs={
                                       # 'class': 'form-control',
                                       'placeholder': 'Select Date of Birth'
                                   }
                               ))
    phone_number = forms.CharField(max_length=13,
                                   required=False,
                                   label="Phone No.",
                                   widget=forms.TextInput(
                                       attrs={
                                           'class': 'form-control',
                                           'placeholder': 'Phone Number',
                                           'autofocus': 'autofocus',
                                       }
                                   ))

    # def __init__(self, user, *args, **kwargs):
    #     self.user = user
    #     # kwargs['instance'] = user
    #     # signup_kwargs = kwargs
    #     # signup_kwargs.pop('instance')
    #     super(UserForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = existing_user_fields(['first_name', 'last_name', 'gender', 'birthday',
                                       'phone_number', 'email'])

        error_messages = {
            'first_name': {
                'required': validators.FIRST_NAME_REQUIRED_ERROR,
            },
            'email': {
                'required': validators.EMAIL_REQUIRED_ERROR,
            },
        }

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = 'id-Profile-Update-Form'
        helper.form_method = 'POST'
        # helper.form_action = reverse('customer:profile-update')
        helper.layout = Layout(
            Row(
                Column('first_name', css_class="form-group col-sm-5 mb-0"),
                Column('last_name', css_class='form-group col-sm-5 mb-0'),
                css_class='form-row'
            ),
            InlineRadios('gender', css_class="form-group"),
            Field('birthday', css_class="form-group col-md-9 mb-0"),
            Field('phone_number', css_class="form-group col-md-10 mb-0"),
            Field('email', css_class="form-group col-md-10 mb-0"),
            Row(
                Submit('submit', 'Save', css_class="form-group btn col-md-offset-2 col-md-2 mb-0",
                       css_id='id-Profile-Save'),
                Reset('reset', 'Reset', css_class='form-group btn col-md-offset-2 col-md-2 mb-0 btn-danger')
            )
        )
        return helper
