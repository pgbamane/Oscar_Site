# from oscar.apps.customer.views import AccountRegistrationView as CoreAccountRegistrationView
from allauth.account.views import SignupView as CoreSignupView

from oscar.apps.customer.views import ProfileUpdateView as CoreProfileUpdateView, ProfileView as CoreProfileView
from apps.customer.forms import SignupForm
# from oscar.apps.customer.views import *

from django.utils.translation import ugettext_lazy as _
# from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from allauth.utils import get_form_class
from .forms import SignupForm, UserForm, ProfileForm
from Oscar_Site import settings
from oscar.core.compat import (
    existing_user_fields, get_user_model
)

User = get_user_model()


class SignupView(CoreSignupView):
    template_name = "account/signup.html"
    form_class = SignupForm
    # redirect_field_name = None
    success_url = reverse_lazy('account_login')

    # success_url = reverse_lazy('promotions:home')

    # def get_form_class(self):
    #     return get_form_class(settings.FORMS, 'signup', self.form_class)

    # def get_success_url(self):
    #     ret = self.success_url
    #     return ret

    def get_context_data(self, **kwargs):
        context_data = super(SignupView, self).get_context_data(**kwargs)
        context_data['form_title'] = "Signup here"
        return context_data

    def form_valid(self, form):
        return super(SignupView, self).form_valid(form)
        # self.customer_final = form.save(self.request)
        # return HttpResponseRedirect(redirect_to=self.get_success_url())

    def post(self, request, *args, **kwargs):
        return super(SignupView, self).post(request, *args, **kwargs)


# # ProfileForm = SignupForm
#
#
class ProfileView(CoreProfileView):
    def get_profile_fields(self, user):
        field_data = []

        # sort the fields in custom order
        additional_fields = list(User._meta.additional_fields)
        SORT_ORDER = {'gender': 0, 'phone_number': 1, 'address': 2, 'locality': 3,
                      'city': 4, 'district': 5, 'state': 6, 'pincode': 7}

        additional_fields.sort(key=lambda val: SORT_ORDER[val])

        # Check for custom user model
        for field_name in additional_fields:
            field_data.append(
                self.get_model_field_data(user, field_name))

        # Check for profile class
        # profile_class = get_profile_class()
        # if profile_class:
        #     try:
        #         profile = profile_class.objects.get(user=user)
        #     except ObjectDoesNotExist:
        #         profile = profile_class(user=user)
        #
        #     field_names = [f.name for f in profile._meta.local_fields]
        #     for field_name in field_names:
        #         if field_name in ('user', 'id'):
        #             continue
        #         field_data.append(
        #             self.get_model_field_data(profile, field_name))

        return field_data


class ProfileUpdateView(CoreProfileUpdateView):
    form_class = ProfileForm
    # template_name = 'account/signup.html'
    template_name = 'customer/profile/profile_form.html'
    communication_type_code = 'EMAIL_CHANGED'
    page_title = _('Edit Profile')
    active_tab = 'profile'
    success_url = reverse_lazy('customer:profile-view')

    # def get(self, request, *args, **kwargs):
    #     return super().get(self, request, *args, **kwargs)
    # # def __init__(self):
    #     super().__init__(self)
# def get_profile_fields(self, customer_final):
#     field_data = []
# #
# #     # Check for custom customer_final model
# #     for field_name in User._meta.additional_fields:
# #         field_data.append(
# #             self.get_model_field_data(customer_final, field_name))
# #
# #     # Check for profile class
# #     profile_class = get_profile_class()
# #     if profile_class:
# #         try:
# #             profile = profile_class.objects.get(customer_final=customer_final)
# #         except ObjectDoesNotExist:
# #             profile = profile_class(customer_final=customer_final)
# #
# #         field_names = [f.name for f in profile._meta.local_fields]
# #         for field_name in field_names:
# #             if field_name in ('customer_final', 'id'):
# #                 continue
# #             field_data.append(
# #                 self.get_model_field_data(profile, field_name))
# #
# #     return field_data
# #
# # def get_model_field_data(self, model_class, field_name):
# #     """
# #     Extract the verbose name and value for a model's field value
# #     """
# #     field = model_class._meta.get_field(field_name)
# #     if field.choices:
# #         value = getattr(model_class, 'get_%s_display' % field_name)()
# #     else:
# #         value = getattr(model_class, field_name)
# #     return {
# #         'name': getattr(field, 'verbose_name'),
# #         'value': value,
# #     }
# #
# # def get_context_data(self, **kwargs):
# #     ctx = super(ProfileUpdateView, self).get_context_data(**kwargs)
# #     ctx['profile_fields'] = self.get_profile_fields(self.request.customer_final)
# #     return ctx
