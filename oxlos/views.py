from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render, get_object_or_404

from account.decorators import login_required

from .models import Project, Task, Item


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "homepage.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"projects": Project.objects.all()})


@login_required
def project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "project.html", {
        "project": project,
        "is_member": project.team.is_member(request.user)
    })


@login_required
def join_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.team.add_member(request.user, by=request.user)
    return redirect(request.GET.get("next", reverse("project", args=[pk])))


@login_required
def task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "task.html", {
        "task": task,
        "items_count": task.items_count(),
        "your_answers_count": task.user_answers_count(request.user),
        "participant_count": task.participant_count(),
        "total_questions_answered": task.total_questions_answered(),
        "distinct_items_answers": task.distinct_items_answers(),
        "is_member": task.project.team.is_member(request.user)
    })


@login_required
def item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    is_member = item.task.project.team.is_member(request.user)
    if request.method == "POST" and is_member:
        item.add_answer(by=request.user, answers=request.POST.getlist("answers"))
        next_item = item.task.next_item(request.user)
        if next_item:
            return redirect("item", pk=next_item.pk)
        else:
            return render(request, "item.html", {
                "project": item.task.project,
                "task": item.task,
                "item": next_item,
                "is_member": is_member,
                "answer_count": item.task.user_answers_count(request.user)
            })
    return render(request, "item.html", {
        "project": item.task.project,
        "task": item.task,
        "item": item,
        "is_member": is_member,
        "answer_count": item.task.user_answers_count(request.user)
    })


@login_required
def item_random(request, pk):
    task = get_object_or_404(Task, pk=pk)
    next_item = task.next_item(request.user)
    if next_item:
        return redirect("item", pk=next_item.pk)
    return render(request, "item.html", {
        "project": task.project,
        "task": task,
        "item": next_item,
        "is_member": task.project.team.is_member(request.user)
    })
