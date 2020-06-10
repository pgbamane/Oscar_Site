from allauth.account.views import SignupView as CoreSignupView
from crispy_forms.utils import render_crispy_form
from django.template.context_processors import csrf
from jsonview.decorators import json_view
from oscar.apps.customer.views import ProfileUpdateView as CoreProfileUpdateView, ProfileView as CoreProfileView
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from apps.customer.forms.account_forms import SignupForm, ProfileForm
from oscar.core.compat import (get_user_model)

User = get_user_model()

SIGNUP_PAGE_MESSAGE = "Signup here"


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
        context_data['form_title'] = SIGNUP_PAGE_MESSAGE
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
        SORT_ORDER = {'gender': 0, 'phone_number': 1, 'birthday': 2}

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
    template_name = 'customer/profile/profile_form.html'
    communication_type_code = 'EMAIL_CHANGED'
    page_title = _('Edit Profile')
    active_tab = 'profile'
    success_url = reverse_lazy('customer:profile-view')

    @json_view
    def form_invalid(self, form):
        # resp = {}
        # RequestContext ensures CSRF token is placed in newly rendered form_html
        csrf_context = {}
        csrf_context.update(csrf(self.request))
        profile_form_html = render_crispy_form(form, context=csrf_context)
        # resp['form'] = profile_form_html
        return {'form': profile_form_html}
