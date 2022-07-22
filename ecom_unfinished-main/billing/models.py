from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save

from accounts.models import GuestEmail
User = settings.AUTH_USER_MODEL

# Create your models here.

class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id', None)
        obj = None; created = None
        if user.is_authenticated:
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)

        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(post_save_user_receiver, sender=User)
