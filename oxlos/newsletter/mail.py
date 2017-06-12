import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from pinax.eventlog.models import log

# @@@ remove this before breaking app out
from oxlos.models import Project

from .models import NewsletterSetting


def send_newsletter(newsletter_setting, test_email=None, dry_run=False):
    from_email = "oxlos@jtauber.com"  # @@@ parameterise
    user = newsletter_setting.user

    subject = "oxlos newsletter"  # @@@ parameterise

    if test_email is not None:
        subject += " [Test]"

    last_sent = newsletter_setting.last_sent

    if last_sent is None:
        last_sent = timezone.now() - datetime.timedelta(days=7)

    if test_email is None and last_sent > timezone.now() - datetime.timedelta(days=1):
        # don't send twice within a day
        return

    # @@@ before breaking this app out, we need to work out how best to provide
    # @@@ this template context
    ctx = {
        "projects": Project.objects.all()
    }

    message_html = render_to_string("email/newsletter.html", ctx)
    message_plaintext = render_to_string("email/newsletter.txt", ctx)

    if not dry_run:
        email = EmailMultiAlternatives(
            subject, message_plaintext, from_email, [test_email or user.email],
        )
        email.attach_alternative(message_html, "text/html")
        email.send()


def send_newsletters(dry_run=False):
    count = 0
    for newsletter_setting in NewsletterSetting.objects.filter(user__is_active=True, active=True):
        send_newsletter(newsletter_setting, dry_run=dry_run)
        if not dry_run:
            newsletter_setting.last_sent = timezone.now()
            newsletter_setting.save()
        count += 1
    log(
        user=None,
        action="NEWSLETTER_SENT",
        extra={"COUNT": count},
    )
    return count


def test_newsletter(newsletter_setting, test_email):
    send_newsletter(newsletter_setting, test_email)
