from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class UserFollows(models.Model):
    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, related_name="followed_by", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "followed_user")
        verbose_name_plural = "User follows"

    def __str__(self):
        return f"{self.user} follows {self.followed_user}"
