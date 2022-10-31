from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from user.models import User


class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    queryset = User.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset
        return self.queryset.filter(id=self.request.user.id)
