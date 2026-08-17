# modelapp\models.py
from django.db import models

class Scan(models.Model):
    disease_class = models.CharField(max_length=100)
    class_key = models.CharField(max_length=50)
    severity = models.CharField(max_length=20)
    recommendation = models.TextField()
    confidence = models.FloatField()
    image_thumbnail = models.TextField()  # base64 data URL, small (~120px) thumbnail
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.disease_class} ({self.confidence:.2f}) @ {self.timestamp}"
    
    
from django.db import models


class Scan(models.Model):
    disease_class = models.CharField(max_length=100)
    class_key = models.CharField(max_length=50)
    severity = models.CharField(max_length=20)
    recommendation = models.TextField()
    confidence = models.FloatField()
    image_thumbnail = models.TextField()  # base64 data URL, small (~120px) thumbnail
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.disease_class} ({self.confidence:.2f}) @ {self.timestamp}"


class CropField(models.Model):
    field_name = models.CharField(max_length=100)
    variety = models.CharField(max_length=100, blank=True, default="")
    area_acres = models.FloatField(null=True, blank=True)
    planting_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.field_name} (planted {self.planting_date})"