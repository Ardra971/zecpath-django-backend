from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Candidate, Employer


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:

        if instance.role == User.Roles.CANDIDATE:
            Candidate.objects.get_or_create(
                user=instance
            )

        elif instance.role == User.Roles.EMPLOYER:
            Employer.objects.get_or_create(
                user=instance,
                defaults={"company_name": ""}
            )