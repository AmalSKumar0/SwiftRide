from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from Administrator.models import *

class Trip(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    passenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trips')
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='driven_trips')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    
    from_location = models.CharField(max_length=255)
    to_location = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, null=True, blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    otp = models.CharField(max_length=6, null=True, blank=True)  # For trip confirmation
    fare = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)  # in kilometers
    time_estimate = models.DurationField(null=True, blank=True)
    
    requested_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    isFinished = models.BooleanField(default=False)

    def __str__(self):
        return f"Trip from {self.from_location} to {self.to_location} ({self.status})"
