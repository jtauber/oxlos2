from django.contrib import admin

from .models import NewsletterSetting


@admin.register(NewsletterSetting)
class NewsletterSettingAdmin(admin.ModelAdmin):
    list_display = ["user", "active", "last_sent"]
