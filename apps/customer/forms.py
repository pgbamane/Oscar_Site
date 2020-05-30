from crispy_forms.bootstrap import InlineRadios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit, Reset
from django.forms import EmailField
from django.urls import reverse
from oscar.apps.customer.forms import *
# from oscar.apps.customer.forms import ProfileForm as UserForm, EmailUserCreationForm as CoreEmailUserCreationForm
from oscar.core.compat import (
    existing_user_fields, get_user_model
)
from allauth.account.forms import SignupForm as CoreSignUpForm, PasswordField
from django.utils.translation import ugettext_lazy as _

# from oscar.core.compat import get_user_model, existing_user_fields
#
# class ProfileForm(UserForm):
#     class Meta:
#         model = User
#         fields = existing_user_fields(['gender', 'address', 'locality', 'phone_number'])

User = get_user_model()

# class EmailUserCreationForm(CoreEmailUserCreationForm):
#     # field_order = ['first_name', 'last_name', 'gender', 'address', 'locality', 'state', 'district', 'city', ]
#
#     def __init__(self, host=None, *args, **kwargs):
#         super(EmailUserCreationForm, self).__init__(host, *args, **kwargs)
#
#     class Meta:
#         model = User
#         fields = ('email', 'gender', 'address', 'locality', 'phone_number')
#
#     def signup(self, request, user):
#         """
#         Invoked at signup time to complete the signup of the user.
#         """
#         pass
#

GENDER_OPTIONS = [
    ('female', 'Female'),
    ('male', 'Male')
]


class SignupForm(CoreSignUpForm):
    first_name = forms.CharField(max_length=30,
                                 label="First Name",
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'placeholder': 'Enter First Name',
                                         'autofocus': 'autofocus',
                                     }))
    last_name = forms.CharField(max_length=30,
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
    # phone_number = forms.CharField(max_length=13, label="Phone No.")

    address = forms.CharField(max_length=255,
                              # help_text="Flat No, Building, Street, Area",
                              label="Address (Flat No, Building, Street, Area)",
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'form-control',
                                      'placeholder': 'Address',
                                      'autofocus': 'autofocus',
                                  }
                              ))
    locality = forms.CharField(max_length=50,
                               # help_text='Locality/Town',
                               label="Locality/Town",
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'Locality',
                                       'autofocus': 'autofocus',
                                   }
                               )
                               )
    state = forms.CharField(max_length=50,
                            label="State",
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'placeholder': 'State',
                                    'autofocus': 'autofocus',
                                }
                            ))
    district = forms.CharField(max_length=50,
                               label="District",
                               widget=forms.TextInput(
                                   attrs={
                                       'class': 'form-control',
                                       'placeholder': 'District',
                                       'autofocus': 'autofocus',
                                   }
                               )
                               )
    city = forms.CharField(max_length=50,
                           # help_text="City or Taluka",
                           label="City/Taluka",
                           widget=forms.TextInput(
                               attrs={
                                   'class': 'form-control',
                                   'placeholder': 'City',
                                   'autofocus': 'autofocus',
                               }
                           ))
    pincode = forms.CharField(max_length=10,
                              # help_text="Pincode stored as Chars",
                              label="Pincode",
                              widget=forms.TextInput(
                                  attrs={
                                      'class': 'form-control',
                                      'placeholder': 'Pincode',
                                      'autofocus': 'autofocus',
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

    # primary key of customer_final
    # email_id = forms.EmailField(max_length=40,
    #                             label="Email ID",
    #                             widget=forms.EmailInput(
    #                                 attrs={
    #                                     'class': 'form-control',
    #                                     'placeholder': 'Email ID'
    #                                 }
    #                             )
    #                             )

    field_order = ['first_name', 'last_name', 'gender', 'address', 'locality', 'state', 'district', 'city',
                   'pincode', 'phone_number', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['password2'] = PasswordField(label=_("Confirm Password"))
        self.fields['email'] = EmailField(label=_('Email ID'),
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
        # helper.field_class = "col-md-6"
        # helper.label_class = "col-md-6"
        # helper.
        helper.layout = Layout(
            Row(
                Column('first_name', css_class="form-group col-sm-5 mb-0"),
                Column('last_name', css_class='form-group col-sm-5 mb-0'),
                css_class='form-row'
            ),
            InlineRadios('gender', css_class="form-group"),
            Field('address', css_class="form-group col-md-9 mb-0"),
            Row(
                Column('locality', css_class="form-group col-sm-5 mb-0"),
                Column('state', css_class='form-group col-sm-5 mb-0'),
                css_class='form-row'
            ),
            # Field('locality'),
            # 'state',
            Row(
                Column('district', css_class="form-group col-md-4 mb-0"),
                Column('city', css_class="form-group col-md-3 mb-0"),
                Column('pincode', css_class="form-group col-md-3 mb-0"),
                css_class="form-row"
            ),
            Field('phone_number', css_class="form-group col-md-10 mb-0"),
            Field('email', css_class="form-group col-md-10 mb-0"),
            Field('password1', css_class="form-group col-md-10 mb-0"),
            Field('password2', css_class="form-group col-md-10 mb-0"),
            # Column('city'),
            Row(
                Submit('submit', 'Sign Up', css_class="form-group btn col-md-offset-2 col-md-2 mb-0",
                       css_id='sign-up-id'),
                Reset('reset', 'Reset', css_class='form-group btn col-md-offset-2 col-md-2 mb-0 btn-danger')
            )
        )
        # helper.attrs('novalidate')
        return helper
