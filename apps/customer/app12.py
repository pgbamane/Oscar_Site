# from django.conf.urls import url
# from oscar.apps.customer.app import CustomerApplication as CoreCustomerApplication
# from django.urls import path, include
#
# # from allauth.utils import ge
# from oscar.core.loading import get_class
# from .views import SignupView
#
#
# class CustomerApplication(CoreCustomerApplication):
#     signup_view = SignupView
#
#     def get_urls(self):
#         urls = super(CustomerApplication, self).get_urls()
#         urls += [
#             url(r'^signup/$', self.signup_view.as_view(), name='signup'),
#             url(r'^accounts/', include('allauth.urls')),
#
#         ]
#         return self.post_process_urls(urls)
#
#
# application = CustomerApplication()
