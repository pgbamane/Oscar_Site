import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

BIRTHDAY_INVALID_ERROR = 'Birthday is invalid.'
DATE_INCORRECT_FORMAT_ERROR = 'Incorrect date format, should be DD-MM-YYYY'
EMAIL_REQUIRED_ERROR = 'Email is required.'
EMAIL_INVALID_ERROR = 'Enter a valid email address.'
EMAIL_INVALID_DOMAIN_ERROR = 'Email address should contain a valid domain(Gmail, Yahoo, Only).'
EMAIL_ALREADY_TAKEN_ERROR = "A user is already registered with this e-mail address."
PASSWORD_NOT_SAME_ERROR = "You must type the same password each time."

DATE_FORMAT = "%d-%m-%Y"


def validate_date_format(date):
    try:
        datetime.datetime.strptime(str(date), DATE_FORMAT)
    except ValueError:
        raise ValidationError(_(DATE_INCORRECT_FORMAT_ERROR))
