from oscar.apps.customer.models import *  # noqa isort:skip

# The order that model classes are imported makes a difference,
# with only the first one for a given class name being registered.
# So, user model is already registered using migrate of users app,
# here it will not registered again from import customer models
