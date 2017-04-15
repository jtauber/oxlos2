from django.contrib import admin

from .models import Project, Task, Item, ItemResponse


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name"]
    exclude = ["team"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "project"]


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["id", "task", "data"]


@admin.register(ItemResponse)
class ItemResponseAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "item", "created_at", "answer"]
    list_filter = ["user"]
