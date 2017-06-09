import sys

from django.core.management.base import BaseCommand

from oxlos.newsletter.mail import test_newsletter
from oxlos.newsletter.models import NewsletterSetting


class Command(BaseCommand):
    help = "Send test newsletter."

    def add_arguments(self, parser):
        parser.add_argument("username")
        parser.add_argument("email")

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]

        try:
            newsletter_setting = NewsletterSetting.objects.get(user__username=username)
        except NewsletterSetting.DoesNotExist:
            sys.exit("Unable to find user")
        else:
            print(f"sending newsletter for {username} to {email}...")
            test_newsletter(newsletter_setting, email)
            print("sent.")
