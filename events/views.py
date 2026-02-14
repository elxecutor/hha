from datetime import timedelta
from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils import timezone
from events.models import Event
from events.utils import get_upcoming_occurrences


def home(request):
    # Get upcoming occurrences
    upcoming_occurrences = get_upcoming_occurrences(days_ahead=60)

    # Simple pagination with fixed page size of 6
    paginator = Paginator(upcoming_occurrences, 6)
    page = request.GET.get('page', 1)
    occurrence_page = paginator.get_page(page)

    context = {'events': occurrence_page}
    return render(request, 'events/events.html', context)
