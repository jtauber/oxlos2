from django.core.management.base import BaseCommand

from oxlos.newsletter.mail import send_newsletters


class Command(BaseCommand):
    help = "Send newsletters."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            dest="dry_run",
            default=False,
            help="Test creation of newsletter emails (without sending)"
        ),

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        print("sending newsletters...")
        count = send_newsletters(dry_run=dry_run)
        print(f"{count} sent.")
