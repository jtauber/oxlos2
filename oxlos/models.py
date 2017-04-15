from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

from jsonfield import JSONField
from pinax.teams.models import SimpleTeam


class Project(models.Model):
    name = models.CharField(max_length=250)
    team = models.ForeignKey(SimpleTeam)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.team = SimpleTeam.objects.create(
                member_access=SimpleTeam.MEMBER_ACCESS_OPEN,
                manager_access=SimpleTeam.MANAGER_ACCESS_ADD
            )
        return super(Project, self).save(*args, **kwargs)


class Task(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=250)
    description = models.TextField()
    description_html = models.TextField(blank=True, editable=False)

    def __str__(self):
        return self.name


class Item(models.Model):
    task = models.ForeignKey(Task)
    data = JSONField()


class ItemResponse(models.Model):
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now)
    answer = models.TextField()
