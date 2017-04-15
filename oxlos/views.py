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
def task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "task.html", {
        "task": task,
        "is_member": task.project.team.is_member(request.user)
    })


@login_required
def item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    is_member = item.task.project.team.is_member(request.user)
    if request.method == "POST" and is_member:
        item.add_answer(by=request.user, data=request.POST.getlist("answers"))
        return redirect("item", kwargs={"pk": task.item_set.order_by("?").first().pk})
    return render(request, "item.html", {
        "item": item,
        "is_member": is_member
    })


@login_required
def item_random(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return redirect("item", kwargs={"pk": task.item_set.order_by("?").first().pk})
