# from oscar.apps.customer_12.views import *
# from oscar.apps.customer_12.views import ProfileUpdateView as CoreProfileUpdateView
# from apps.customer_final.forms import SignupForm
# from django.utils.translation import ugettext_lazy as _
#
#
# # ProfileForm = SignupForm
#
#
# class ProfileUpdateView(CoreProfileUpdateView):
#     # form_class = SignupForm
#     # template_name = 'account/signup.html'
#     # communication_type_code = 'EMAIL_CHANGED'
#     # page_title = _('Edit Profile')
#     # active_tab = 'profile'
#     # success_url = reverse_lazy('customer_12:profile-view')
#
#     def get(self, request, *args, **kwargs):
#         return super().get(self, request, *args, **kwargs)
#     # def __init__(self):
#     #     super().__init__(self)
# # def get_profile_fields(self, customer_final):
# #     field_data = []
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
