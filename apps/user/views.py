from django.shortcuts import render

# Create your views here.
from allauth.account.views import SignupView as AllAuthSignupView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from allauth.utils import get_form_class
from .forms import SignupForm
from Oscar_Site import settings


class SignupView(AllAuthSignupView):
    template_name = "account/signup.html"
    form_class = SignupForm
    redirect_field_name = None
    success_url = reverse_lazy('home')

    # def get_form_class(self):
    #     return get_form_class(settings.FORMS, 'signup', self.form_class)

    def get_success_url(self):
        ret = self.success_url
        return ret

    def get_context_data(self, **kwargs):
        context_data = super(SignupView, self).get_context_data(**kwargs)
        context_data['form_title'] = "Signup here"
        return context_data

    def form_valid(self, form):
        return super(SignupView, self).form_valid(form)
        # self.user = form.save(self.request)
        # return HttpResponseRedirect(redirect_to=self.get_success_url())

    def post(self, request, *args, **kwargs):
        return super(SignupView, self).post(request, *args, **kwargs)
