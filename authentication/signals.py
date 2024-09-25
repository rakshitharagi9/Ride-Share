# authentication/signals.py
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import PassengerDTable
from django.contrib.auth.models import User

@receiver(pre_delete, sender=PassengerDTable)
def notify_user_on_ride_cancel(sender, instance, **kwargs):
    ride = instance
    username1 = ride.username1
    username2 = ride.username2
    
    # Find email of username2
    try:
        user2 = User.objects.get(username=username2)
        username2_email = user2.email
        
        # Send notification email to username2
        send_mail(
            subject='Ride Cancellation Notification',
            message=f'Hi {username2},\n\n{username1} has canceled the ride.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[username2_email],
        )
    except User.DoesNotExist:
        # Handle case where username2 does not exist
        pass
