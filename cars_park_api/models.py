from django.db import models
from datetime import datetime
from django.utils.timezone import make_aware

DATE_FORMAT = '%d-%m-%Y'


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField('date created', auto_now_add=True)
    updated_at = models.DateTimeField('date updated', auto_now=True)

    class Meta:
        abstract = True


class Driver(TimeStampMixin):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    @classmethod
    def get_created_at__gte(cls, date_str):
        date = make_aware(datetime.strptime(date_str, DATE_FORMAT))
        return cls.objects.filter(created_at__gte=date)

    @classmethod
    def get_created_at__lte(cls, date_str):
        date = make_aware(datetime.strptime(date_str, DATE_FORMAT))
        return cls.objects.filter(created_at__lte=date)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Vehicle(TimeStampMixin):
    driver = models.ForeignKey(Driver, blank=True, null=True, on_delete=models.SET_NULL)
    make = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    plate_number = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.make} {self.model} {self.plate_number}"
