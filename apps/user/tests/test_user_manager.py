from django.contrib.auth import get_user_model
from django.test import TestCase


class UserManagerTestCase(TestCase):

    def test_create_super_user(self):
        User = get_user_model()
        user = User.objects.create_superuser(
            # first_name='Pradnya',
            #                             last_name='Bamane',
            email='pradnya@gmail.com',
            phone_number='9545065515',
            # gender='female',
            password="satputeps"
        )
        # self.assertEqual(user.first_name, 'Pradnya')
        self.assertEqual(user.phone_number, '9545065515')
        self.assertEqual(user.email, 'pradnya@gmail.com')
        self.assertEqual(user.get_username(), user.email)
        self.assertEqual(user.check_password('satputeps'), True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)
