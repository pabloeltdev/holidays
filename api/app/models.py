from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, \
    MinLengthValidator
from .validators import file_size


def image_name(instance, filename):
    return "holidays/{}".format(
        instance.country+'_'+instance.title
    )


class Holiday(models.Model):
    title = models.CharField(max_length=100, validators=[
        MinLengthValidator(3)
    ])
    description = models.CharField(max_length=5000, validators=[
        MinLengthValidator(50)
    ])
    country = models.CharField(max_length=30, validators=[
        MinLengthValidator(4)
    ])
    event_day = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(31),
    ])
    event_month = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(12),
    ])
    image = models.ImageField(
        null=True,
        upload_to=image_name,
        validators=[
            file_size
        ])

    def __str__(self):
        return f'[{self.country}] {self.title}'

    def event_long_month(self):
        month_names = [
            'January', 'February', 'March',
            'April', 'May', 'June', 'July',
            'August', 'September', 'October',
            'November', 'December'
        ]
        return month_names[self.event_month - 1]

    class Meta:
        unique_together = ('title', 'country',)
