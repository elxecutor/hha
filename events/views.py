from datetime import timedelta
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone
from events.models import Event


def home(request):
    now = timezone.now()
    today = now.date()
    two_months_later = now + timedelta(days=60)
    
    # Retrieve all events (unchanged, but you can add filtering if needed)
    events = Event.objects.all().order_by('start_time')
    
    # Build a list of upcoming occurrences using list comprehension
    upcoming_occurrences = sorted(
        [
            {'event': evt, 'date': occ.date(), 'days_until': (occ.date() - today).days}
            for evt in events
            for occ in evt.get_occurrences(now, two_months_later)
        ],
        key=lambda x: (x['date'], x['event'].start_time)
    )

    # Simple pagination with fixed page size of 6
    paginator = Paginator(upcoming_occurrences, 6)
    page = request.GET.get('page', 1)
    occurrence_page = paginator.get_page(page)

    context = {'events': occurrence_page}
    return render(request, 'events/events.html', context)
