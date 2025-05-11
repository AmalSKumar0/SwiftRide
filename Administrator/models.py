from django.db import models
from django.utils.timezone import now

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  
    approved = models.BooleanField(default=True)
    phone_no = models.CharField(max_length=15, unique=True)
    rights = models.CharField(
        max_length=50,
        choices=[('admin', 'Admin'), ('user', 'User'), ('driver', 'Driver')],
        default='customer'
    )
    created_at = models.DateTimeField(default=now, editable=False)
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    
class Vehicle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicles")  
    vehicle_type = models.CharField(
        max_length=20,
        choices=[
            ('Auto Rickshaw', 'Auto Rickshaw'),
            ('Economy Car', 'Economy Car'),
            ('Sedan', 'Sedan'),
            ('Luxury Car', 'Luxury Car')
        ]
    )
    manufacture_date = models.DateField()
    license_number = models.CharField(max_length=50, unique=True)
    vehicle_number = models.CharField(max_length=20, unique=True)
    vehicle_image = models.ImageField(upload_to='uploads/vehicles/')
    current_location = models.CharField(max_length=255, default="")  
    is_active = models.BooleanField(default=False) 

    def __str__(self):
        return self.vehicle_type

class VehiclePrice(models.Model):
    base_fare = models.FloatField(default=30)
    base_distance = models.FloatField(default=1.5)
    rate_per_km = models.FloatField(default=15)
    commission_rate = models.FloatField(default=0.10)
    created_at = models.DateTimeField(default=now)
    vehicle_type = models.CharField(
        max_length=20,
        choices=[
            ('Auto Rickshaw', 'Auto Rickshaw'),
            ('Economy Car', 'Economy Car'),
            ('Sedan', 'Sedan'),
            ('Luxury Car', 'Luxury Car')
        ]
    )

    def __str__(self):
        return "Pricing Rules"

class Review(models.Model):
    passenger = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='given_reviews')
    driver = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='received_reviews')
    vehicle = models.ForeignKey('Vehicle', on_delete=models.SET_NULL, null=True, related_name='vehicle_reviews')
    
    rating = models.PositiveSmallIntegerField()  
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.passenger} rated {self.driver} - {self.rating} stars"