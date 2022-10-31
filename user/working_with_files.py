import csv
import datetime

import xmltodict

from django.contrib.auth import get_user_model
from django.utils import timezone


def remove_data_in_brackets(word):
    if all(bracket in word for bracket in ["(", ")"]):
        start_slice = word.find("(")
        end_slice = word.rfind(")")
        ignored_data = word[start_slice:end_slice + 1]
        return word.replace(ignored_data, '').strip()
    return word


def load_user_data():
    """
    To load user data from test_task.xml and test_task.csv
    Enter in Terminal:
    python manage.py shell
    from user.working_with_files import load_user_data
    load_user_data()
    """
    user_list = []

    with open("./user/test_task.xml", 'r', encoding='utf-8') as file:
        my_xml = file.read()
        my_dict = xmltodict.parse(my_xml)
        for user in my_dict["user_list"]["user"]["users"]["user"]:
            if user["first_name"] is not None or user["last_name"] is not None:
                for key in ["first_name", "last_name"]:
                    if user[key] is not None:
                        user[key] = remove_data_in_brackets(user[key])
                del user["@id"]
                user_list.append(user)

    with open("./user/test_task.csv", 'r') as file:
        csv_file = csv.DictReader(file)
        for row in csv_file:
            if row["username"] != '':
                row["username"] = remove_data_in_brackets(row["username"])
                if row["date_joined"] != '':
                    row["date_joined"] = datetime.datetime.fromtimestamp(int(row["date_joined"]), tz=timezone.utc)
                else:
                    row["date_joined"] = datetime.datetime.now(tz=timezone.utc)

                for user in user_list:  # collect a complete set of user data
                    if user["last_name"] is not None:
                        normalized_username = row["username"].lower()
                        normalized_last_name = user["last_name"].lower()
                        if normalized_last_name in normalized_username:
                            user.update(row)
                    else:
                        if user["first_name"][0] in row["username"] and len(row["username"]) == 2:
                            user.update(row)

    for user in user_list:
        get_user_model().objects.create_user(**user)
