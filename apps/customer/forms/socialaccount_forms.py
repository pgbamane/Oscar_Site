from allauth.socialaccount.forms import SignupForm as CoreSignupForm
# from crispy_forms import helper
from crispy_forms.bootstrap import InlineField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Field, Submit
from django.urls import reverse


class SignupForm(CoreSignupForm):
    """
    override to support crispy form
    """

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_id = "signup_form"
        helper.form_class = "signup"
        helper.form_method = "POST"
        helper.form_action = reverse('socialaccount_signup')
        helper.layout = Layout(
            'email',
            # , css_class="form-group col-md-3 mb-0"),
            Submit('submit', 'Sign Up')
            # , css_class="form-group btn col-md-2 mb-0",
            #        css_id='sign-up-id'),
        )
        return helper
