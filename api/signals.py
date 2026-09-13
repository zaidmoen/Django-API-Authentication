import logging
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger("api")

@receiver(post_save, sender=get_user_model())
def log_user_created(sender, instance, created, **kwargs):
    if created: logger.info("User created: id=%s username=%s", instance.pk, instance.username)

