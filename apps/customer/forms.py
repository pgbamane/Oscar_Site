from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, Reset
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

User = get_user_model()

FIRST_NAME_REQUIRED_ERROR = 'First Name is required.'
LAST_NAME_REQUIRED_ERROR = ['Last Name is required.']
EMAIL_REQUIRED_ERROR = 'Email is required.'


class SignupForm(CoreSignUpForm):
    first_name = forms.CharField(max_length=30,
                                 label="First Name",
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Enter First Name',
                                         'autofocus': 'autofocus',
                                     }),
                                 error_messages={
                                     'required': FIRST_NAME_REQUIRED_ERROR
                                 })
    last_name = forms.CharField(max_length=30,
                                label="Last Name",
                                widget=forms.TextInput(
                                    attrs={
                                        'class': 'form-control',
                                        'placeholder': 'Enter Last Name',
                                        'autofocus': 'autofocus',
                                    }),
                                error_messages={
                                    'required': LAST_NAME_REQUIRED_ERROR
                                })

    gender = forms.ChoiceField(label="Gender",
                               choices=GENDER_OPTIONS,
                               initial=FEMALE,
                               widget=forms.RadioSelect()
                               )
    birthday = forms.DateField(label='Birthday',
                               widget=DatePickerInput(
                                   options={
                                       'format': "DD/MM/YYYY",
                                       'minDate': '01/01/1960',
                                   },
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Select Date of Birth'
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
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password2'] = PasswordField(label=_("Confirm Password"))
        self.fields['email'] = forms.EmailField(label=_('Email ID'),
                                                widget=forms.EmailInput(
                                                    attrs={
                                                        'class': 'form-control',
                                                        'placeholder': 'Email ID'
                                                    }
                                                ))

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
                Column('first_name', css_class="form-group col-md-5 mb-0"),
                Column('last_name', css_class='form-group col-md-5 mb-0'),
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
                'required': FIRST_NAME_REQUIRED_ERROR,
            },
            'email': {
                'required': EMAIL_REQUIRED_ERROR,
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
