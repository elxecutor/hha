from django.contrib import admin
from events.models import Event
from django.utils import timezone
from datetime import timedelta


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'start_time', 'end_time', 'location', 'is_special', 'get_upcoming_occurrences')
    list_filter = ('is_special', 'start_date', 'location', 'recurrence')
    search_fields = ('name', 'description', 'location')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('slug',)
    list_per_page = 20
    date_hierarchy = 'start_date'
    ordering = ('start_date', 'start_time')

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'start_date', 'start_time', 'end_time', 'location', 'image')
        }),
        ('Recurrence', {
            'fields': ('recurrence',),
            'description': 'Set recurrence rules for repeating events. Leave empty for one-time events. Use formats like "RRULE:FREQ=WEEKLY;BYDAY=SU" for weekly on Sunday, or "RRULE:FREQ=MONTHLY;BYMONTHDAY=1" for monthly on the 1st.',
            'classes': ('collapse',)
        }),
        ('Special Event Options', {
            'fields': ('is_special',),
            'classes': ('collapse',),
        }),
    )

    def get_upcoming_occurrences(self, obj):
        now = timezone.now()
        future = now + timedelta(days=30)
        occurrences = obj.get_occurrences(now, future)
        if occurrences:
            return f"{len(occurrences)} upcoming"
        return "No upcoming"
    get_upcoming_occurrences.short_description = 'Upcoming Events'


admin.site.register(Event, EventAdmin)
