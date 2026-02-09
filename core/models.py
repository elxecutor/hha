from django.db import models
from django.core.validators import RegexValidator

PHONE_REGEX = r'^\+234\d{10}$'

class Leader(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, validators=[RegexValidator(PHONE_REGEX)])

    def __str__(self):
        return self.name

class Worker(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, validators=[RegexValidator(PHONE_REGEX)])

    def __str__(self):
        return self.name