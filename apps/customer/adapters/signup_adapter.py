from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field
from django.forms import ValidationError

from apps.customer import validators


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
            raise ValidationError(validators.EMAIL_INVALID_DOMAIN_ERROR)
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
        birthday = form_data.get('birthday')
        phone_number = form_data.get('phone_number')
        if gender:
            user_field(user, 'gender', gender)
        if birthday:
            # user_field(user, 'birthday', birthday)
            user.birthday = birthday
        if phone_number:
            user_field(user, 'phone_number', phone_number)
        # finally save User with all fields
        user.save()
        return user
