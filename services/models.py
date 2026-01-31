from django.db import models


class Service(models.Model):
    class Type(models.IntegerChoices):
        CLEANING = 1, "Cleaning"
        REPAIR = 2, "Repair"
        MOVING = 3, "Moving"
        CONSTRUCTION = 4, "Construction"
        OTHER = 5, "Other"

    title = models.CharField(max_length=60)
    is_active = models.BooleanField(default=True)
    service_type = models.IntegerField(choices=Type.choices)
    description = models.TextField(blank=True, null=True)

    base_duration_minutes = models.PositiveIntegerField(default=60)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title