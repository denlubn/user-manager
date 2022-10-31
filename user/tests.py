import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from .working_with_files import remove_data_in_brackets, load_user_data


class DataCollectionTests(TestCase):
    def test_remove_data_in_brackets(self):
        test_words = {"Ukd ((brs)s) ": "Ukd", "(mal)igg": "igg", " (afg) ": ""}

        for word, correct_word in test_words.items():
            self.assertEqual(remove_data_in_brackets(word), correct_word)

    def test_load_user_data(self):
        load_user_data()
        users = get_user_model().objects.all()

        for user in users:
            # test open .xml
            self.assertTrue(user.first_name is not None or user.last_name is not None)
            self.assertFalse(hasattr(user, "@id"))

            # test open .csv
            self.assertTrue(hasattr(user, "username"))
            self.assertTrue(isinstance(user.date_joined, datetime.datetime))

            # test collect a complete set
            if user.last_name:
                self.assertTrue(user.last_name.lower() in user.username.lower())
            else:
                self.assertTrue(user.first_name[0] in user.username and len(user.username) == 2)
