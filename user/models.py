from tempfile import NamedTemporaryFile
from urllib.parse import urlparse
from urllib.request import urlopen, Request

from django.contrib.auth.models import AbstractUser
from django.core.files import File
from django.db import models


class User(AbstractUser):
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    avatar = models.URLField()
    avatar_file = models.ImageField(upload_to='avatars', null=True)

    def save(self, *args, **kwargs):
        if self.avatar and not self.avatar_file:
            img_temp = NamedTemporaryFile(delete=True)
            req = Request(
                url=self.avatar,
                headers={'User-Agent': 'XYZ/3.0'}
            )
            img_temp.write(urlopen(req, timeout=10).read())
            img_temp.flush()
            filename = urlparse(self.avatar).path.split('/')[-1]
            self.avatar_file.save(filename, File(img_temp))
        return super(User, self).save(*args, **kwargs)
