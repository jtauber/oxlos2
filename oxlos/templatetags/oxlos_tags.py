from django import template

register = template.Library()


@register.filter
def is_member(project, user):
    return project.team.is_member(user)
