from django.utils import timezone
from datetime import timedelta
from events.models import Event


def get_upcoming_occurrences(days_ahead=60, limit=None):
    """
    Get upcoming event occurrences within the next days_ahead days.
    Returns a sorted list of dicts: {'event': event, 'date': date, 'days_until': int}
    """
    now = timezone.now()
    today = now.date()
    end_date = now + timedelta(days=days_ahead)

    events = Event.objects.all()
    occurrences = []
    for event in events:
        occs = event.get_occurrences(now, end_date)
        for occ in occs:
            occurrences.append({
                'event': event,
                'date': occ.date(),
                'days_until': (occ.date() - today).days
            })

    # Sort by date and start_time
    occurrences.sort(key=lambda x: (x['date'], x['event'].start_time))

    if limit:
        occurrences = occurrences[:limit]

    return occurrences