from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string


@shared_task
def send_welcome_email(user_pk):
    user = get_user_model().objects.get(id=user_pk)
    context = {
        'email': user.email.split('@')[0],
        'user_pk': user_pk,
    }
    template_name = 'welcome-email.html'
    msg = render_to_string(template_name, context)
    send_mail(
        'Denzel-Fan-Page Registration',
        '',
        'r.marinkov99@gmail.com',
        (user.email, ),
        html_message=msg
    )
