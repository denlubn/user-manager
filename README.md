# User Manager

## Installation

Python3 must be already installed

```shell
git clone https://github.com/denlubn/user-manager.git
cd user-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver # starts Django Server
```

## Create users

Create admin user

```shell
python manage.py createsuperuser
```

Load users from CSV and XML files

```shell
python manage.py shell
from user.working_with_files import load_user_data
load_user_data()
```

I spent 5-8 hours on it