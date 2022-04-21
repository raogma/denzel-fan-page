from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from DenzelProject.profileApp.models import Profile


@receiver(post_save, sender=get_user_model())
def create_profile_after_user_register(sender, instance, created, **kwargs):
    if created:
        profile = Profile(
            user=instance
        )
        profile.save()


@receiver(post_delete, sender=Profile)
def delete_user_after_profile(**kwargs):
    user = get_user_model().objects.get(pk=kwargs['instance'].pk)
    user.delete()
