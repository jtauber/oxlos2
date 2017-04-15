from django.shortcuts import redirect, render, get_object_or_404

from account.decorators import login_required

from .models import Project, Task, Item


def home(request):
    if request.is_authenticated:
        return redirect("dashboard")
    return render("homepage.html")


@login_required
def dashboard(request):
    return render(request, "dashboard.html", {"projects": Project.objects.all()})


@login_required
def project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, "project.html", {"project": project})


@login_required
def task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "task.html", {"task": task})


@login_required
def item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        item.add_answer(by=request.user, data=request.POST.getlist("answers"))
        return redirect("item", kwargs={"pk": task.item_set.order_by("?").first().pk})
    return render(request, "item.html", {"item": item})


@login_required
def item_random(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return redirect("item", kwargs={"pk": task.item_set.order_by("?").first().pk})
