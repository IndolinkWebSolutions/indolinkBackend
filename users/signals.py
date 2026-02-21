from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Welcome to Our Platform 🎉"
        message = f"""
Hi {instance.username},

Your account has been successfully created.

You can now login and start using our free services.

If you did not create this account, please contact support immediately.

Regards,
Team Support
"""
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=True
        )




from django.dispatch import Signal

password_reset_success = Signal()


@receiver(password_reset_success)
def send_password_reset_email(sender, user, **kwargs):
    subject = "Your Password Was Reset Successfully 🔐"
    message = f"""
Hi {user.username},

Your password has been reset successfully.

If this was not you, please contact support immediately.

Regards,
Security Team
"""
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=True
    )
