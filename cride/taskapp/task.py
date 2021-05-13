"""Celery task"""

# Django
from datetime import timedelta
import jwt

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

# celery
from celery.decorators import task, periodic_task
# Models
from cride.rides.models import Ride
from cride.users.models import User


@task(name='send_confimation_email', max_retries=3)
def send_confimation_email(user_pk):
    """Send account verification link to given user"""
    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)
    subject = 'Welcome @{}! verify your accoutn yo start usign Comparte Ride'.format(user.username)
    from_email = 'Comparte Ride <noreply@comparteride.com>'
    to = user.email
    text_content = render_to_string(
        'emails/users/account_verification.html',
        {'token': verification_token, 'user': user}
    )
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(text_content, "text/html")
    msg.send()


def gen_verification_token(user):
    """Create a JWT token that the user can use to verify its accoutn"""
    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token.decode()


@periodic_task(name='disable_finished_ride', run_every=timedelta(seconds=5))
def disable_finished_rides():
    """disable finished rides"""
    now = timezone.now()

    offset = now + timedelta(seconds=5)

    rides = Ride.objects.filter(
        arrival_date__gte=now,
        arrival_date__lte=offset,
        is_active=True
    )
    rides.update(is_active=True)
