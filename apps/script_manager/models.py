from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# Define the Script model
class Script(models.Model):
    # Define choices for the type field
    SCRIPT_TYPE_CHOICES = [
        ('required', 'Required'),
        ('marketing', 'Marketing'),
        ('analytics', 'Analytics'),
    ]

    # Fields for Script model
    code = models.TextField()
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
    )
    script_type = models.CharField(
        max_length=50,
        choices=SCRIPT_TYPE_CHOICES,
    )

    def __str__(self):
        return f"{self.service.name} - {self.get_script_type_display()}"
