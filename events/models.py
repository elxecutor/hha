from datetime import datetime
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.core.exceptions import ValidationError
import recurrence.fields  # django-recurrence

class Event(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, editable=False)
    is_special = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(help_text='Start date of the event.')
    recurrence = recurrence.fields.RecurrenceField(
        null=True,
        blank=True,
        help_text="Set recurrence rules for the event. Leave empty for one-time events."
    )
    start_time = models.TimeField(help_text='Start time of the event.')
    end_time = models.TimeField(help_text='End time of the event.')
    location = models.CharField(max_length=200, help_text='Location of the event.')
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_date', 'start_time']
        indexes = [
            models.Index(fields=['start_date']),
            models.Index(fields=['is_special']),
            models.Index(fields=['start_date', 'is_special']),
        ]

    def clean(self):
        if self.end_time <= self.start_time:
            raise ValidationError('End time must be after start time.')

    def delete(self, *args, **kwargs):
        if self.image:
            storage, path = self.image.storage, self.image.path
            storage.delete(path)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.full_clean()  # Validate before saving
        super().save(*args, **kwargs)

    def get_occurrences(self, range_start, range_end):
        """
        Returns a list of datetime objects representing event occurrences
        between 'range_start' and 'range_end'. For recurring events, uses the
        recurrence field; for one-time events, returns the start_date if it lies within the range.
        """
        if self.recurrence:
            dtstart = timezone.make_aware(datetime.combine(self.start_date, self.start_time))
            return self.recurrence.between(
                range_start,
                range_end,
                dtstart=dtstart,
                inc=True
            )
        else:
            event_datetime = timezone.make_aware(datetime.combine(self.start_date, self.start_time))
            if range_start <= event_datetime <= range_end:
                return [event_datetime]
            return []

    def get_next_occurrence(self, after=None):
        """Get the next occurrence after the given datetime."""
        if after is None:
            after = timezone.now()
        occurrences = self.get_occurrences(after, after + timezone.timedelta(days=365))
        return occurrences[0] if occurrences else None

    def __str__(self):
        return self.name
