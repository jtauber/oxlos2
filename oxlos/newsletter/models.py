from django.db import models

from django.contrib.auth.models import User


class NewsletterSetting(models.Model):

    user = models.ForeignKey(User)
    active = models.BooleanField(default=True)
    last_sent = models.DateTimeField(null=True, blank=True)
