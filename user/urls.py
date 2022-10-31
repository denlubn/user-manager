from django.urls import path

from user.views import UserListView

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
]

app_name = "user"
