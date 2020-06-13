import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

FIRST_NAME_REQUIRED_ERROR = 'First Name is required.'
LAST_NAME_REQUIRED_ERROR = 'Last Name is required.'
BIRTHDAY_INVALID_ERROR = 'Birthday is invalid.'
DATE_INCORRECT_FORMAT_ERROR = 'Incorrect date format, should be DD-MM-YYYY'
EMAIL_REQUIRED_ERROR = 'Email is required.'
EMAIL_INVALID_ERROR = 'Enter a valid email address.'
EMAIL_INVALID_DOMAIN_ERROR = 'Email address should contain a valid domain(Gmail, Yahoo, Only).'
EMAIL_ALREADY_TAKEN_ERROR = "A user is already registered with this e-mail address."
USERFORM_EMAIL_EXISTS_ERROR = "A user with this email address already exists"
PASSWORD1_REQUIRED_ERROR = 'Password is required.'
PASSWORD2_REQUIRED_ERROR = 'Confirm Password is required.'
PASSWORD_NOT_SAME_ERROR = "You must type the same password each time."

DATE_FORMAT = "%d-%m-%Y"


def validate_date_format(date):
    try:
        datetime.datetime.strptime(str(date), DATE_FORMAT)
    except ValueError:
        raise ValidationError(_(DATE_INCORRECT_FORMAT_ERROR))
