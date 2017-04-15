from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User

import markdown

from jsonfield import JSONField
from pinax.teams.models import SimpleTeam


class Project(models.Model):
    name = models.CharField(max_length=250)
    team = models.ForeignKey(SimpleTeam)
    description = models.TextField()
    description_html = models.TextField(blank=True, editable=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.description_html = markdown.markdown(self.description)
        if self.pk is None:
            self.team = SimpleTeam.objects.create(
                member_access=SimpleTeam.MEMBER_ACCESS_OPEN,
                manager_access=SimpleTeam.MANAGER_ACCESS_ADD
            )
        return super(Project, self).save(*args, **kwargs)


class Task(models.Model):
    project = models.ForeignKey(Project, related_name="tasks")
    name = models.CharField(max_length=250)
    description = models.TextField()
    description_html = models.TextField(blank=True, editable=False)
    instructions = models.TextField()
    instructions_html = models.TextField(blank=True, editable=False)
    question_template = models.TextField()

    def __str__(self):
        return self.name

    def next_item(self, user):
        return self.item_set.exclude(itemresponse__user=user).order_by("?").first()

    """
    <div class="stats">
        There are {{ items_count }} items in this task. You have answered
        {{ you_answer_count }}. In total, {{ participant_count }} people
        have participated in this task so far, answering {{ total_questions_answered }}
        questions covering a total of {{ distinct_items_answers }} items.
    </div>
    """
    def items_count(self):
        return self.item_set.count()

    def user_answers_count(self, user):
        return user.itemresponse_set.filter(item__task=self).count()

    def participant_count(self):
        return self.item_set.exclude(itemresponse__isnull=True).values("itemresponse__user").distinct().count()

    def total_questions_answered(self):
        return self.item_set.filter(itemresponse__isnull=False).count()

    def distinct_items_answers(self):
        return self.item_set.filter(itemresponse__isnull=False).distinct().count()

    def save(self, *args, **kwargs):
        self.description_html = markdown.markdown(self.description)
        self.instructions_html = markdown.markdown(self.instructions)
        return super(Task, self).save(*args, **kwargs)


class Item(models.Model):
    task = models.ForeignKey(Task)
    data = JSONField()

    @property
    def question(self):
        return markdown.markdown(
            self.task.question_template.format(**self.data["question"])
        )

    @property
    def choices(self):
        return self.data["choices"]

    def add_answer(self, by, answers):
        return self.itemresponse_set.create(
            user=by,
            answer="|".join(answers)
        )


class ItemResponse(models.Model):
    item = models.ForeignKey(Item)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(default=timezone.now)
    answer = models.TextField()
