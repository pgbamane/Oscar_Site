from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from django.forms import ValidationError


class SignupAdapter(DefaultAccountAdapter):
    def __init__(self, request=None):
        super(SignupAdapter, self).__init__(request)

    def clean_email(self, email):
        email = super(SignupAdapter, self).clean_email(email)
        # def clean_email_id(self):
        # email_id = self.cleaned_data['email_id']
        domain = email.split('@')[1]
        domain_list = ["gmail.com", "yahoo.com", ]
        if domain not in domain_list:
            raise ValidationError('Enter an email address with a valid domain(Gmail, Yahoo, Only)')
        return email

    # def is_ajax(self, request):
    #     return super(SignupAdapter, self).is_ajax(request)

    def ajax_response(self, request, response, redirect_to=None, form=None,
                      data=None):
        return super(SignupAdapter, self).ajax_response(request, response, redirect_to, form,
                                                        data)

    def validate_unique_email(self, email):
        return super(SignupAdapter, self).validate_unique_email(email)

    # def g

    def save_user(self, request, user, form, commit=False):
        print("\nSave User of Signup Adapter")
        user = super(SignupAdapter, self).save_user(request, user, form, commit)
        form_data = form.cleaned_data
        gender = form_data.get('gender')
        address = form_data.get('address')
        locality = form_data.get('locality')
        state = form_data.get('state')
        district = form_data.get('district')
        city = form_data.get('city')
        pincode = form_data.get('pincode')
        phone_number = form_data.get('phone_number')
        # if gender:
        # user_field(user, 'gender', gender)
        # # if address:
        # user_field(user, "address", address)
        # # if locality:
        # user_field(user, "locality", locality)
        # # if state:
        # user_field(user, 'state', state)
        # # if district:
        # user_field(user, 'district', district)
        # # if city:
        # user_field(user, 'city', city)
        # # if pincode:
        # user_field(user, 'pincode', pincode)
        # # if phone_number:
        # user_field(user, 'phone_number', phone_number)

        if gender:
            user.gender = gender
        if address:
            user.address = address
        if locality:
            user.locality = locality
        if state:
            user.state = state
        if district:
            user.district = district
        if city:
            user.city = city
        if pincode:
            user.pincode = pincode
        if phone_number:
            user.phone_number = phone_number

        # finally save User with all fields
        user.save()
        return user

# def clean(self):
#     cleaned_data = super(SignUpForm, self).clean()
#     password = cleaned_data.get('password')
#     confirm_password = cleaned_data.get('confirm_password')
#
#     if password and confirm_password and password != confirm_password:
#         self.add_error('password', 'The Password does not match')


# adp = SignupAdapter()
# adp.ajax_response()
