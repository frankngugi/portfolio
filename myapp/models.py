from django.db import models
from django.contrib.auth.models import User  # Assuming user model

# Create your models here.
class Events(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=4000)
    date = models.DateTimeField('date')


class Member(models.Model):
  member_id = models.AutoField(primary_key=True)
  user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with User
  name = models.CharField (max_length=255, blank=True, null=True)
  email = models.EmailField(unique=True)
  phonenumber = models.IntegerField(default="", max_length=15, blank=True, null=True)
  is_phone_verified = models.BooleanField(default=False)
  address = models.TextField()

  def __str__(self):
        return f"{self.user.username}"

class RegisteredEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_id = models.IntegerField('Event')  # Assuming event ID is an integer

    class Meta:
        unique_together = ('user', 'event_id')  # Ensure a user can't register for the same event twice

    def __str__(self):
        # Consider caching or optimization if this is frequently used
        try:
            event = Events.objects.get(event_id=self.event_id)
            return f"{self.user.username} registered for {event.name}"
        except Events.DoesNotExist:
            # Handle the case where the event doesn't exist (optional)
            return f"{self.user.username} registered for event (ID: {self.event_id})"

class Payment(models.Model):
  payment_id = models.AutoField(primary_key=True)
  registration_id = models.ForeignKey(RegisteredEvent, on_delete=models.CASCADE)
  amount = models.DecimalField(max_digits=10, decimal_places=2)

  mpesa_receipt_number = models.CharField(max_length=50, blank=True, null=True)
  mpesa_sender_phone = models.IntegerField(default=0)
  purpose = models.CharField(max_length=100, blank=True, null=True)
  mpesa_transaction_id = models.CharField(max_length=50, blank=True, null=True)

  
  STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

  status = models.CharField(max_length=10, choices=STATUS_CHOICES)
  payment_date = models.DateTimeField(auto_now_add=True)
