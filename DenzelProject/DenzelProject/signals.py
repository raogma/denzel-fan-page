from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from DenzelProject.profileApp.models import Profile
from DenzelProject.blogPost.models import Post
from DenzelProject.blogPost.models import Comment
from django.core.cache import cache
from DenzelProject.profileApp.tasks import send_welcome_email


@receiver(post_save, sender=get_user_model())
def send_email_after_user_creation(**kwargs):
    if kwargs['created']:
        send_welcome_email.delay(kwargs['instance'].pk)


@receiver(post_save, sender=get_user_model())
def create_profile_after_user_register(**kwargs):
    if kwargs['created']:
        profile = Profile(user=kwargs['instance'])
        profile.save()


@receiver(post_delete, sender=Profile)
def delete_user_after_profile(**kwargs):
    user = get_user_model().objects.get(pk=kwargs['instance'].pk)
    user.delete()

@receiver(post_save, sender=Post)
def clear_cache_post_after_creation(**kwargs):
    cache.clear()


@receiver(post_delete, sender=Post)
def clear_cache_post_upon_removal(**kwargs):
    cache.clear()


    
@receiver(post_save, sender=Comment)
def clear_cache_comment_after_creation(**kwargs):
    cache.clear()


@receiver(post_delete, sender=Comment)
def clear_cache_comment_upon_removal(**kwargs):
    cache.clear()
    