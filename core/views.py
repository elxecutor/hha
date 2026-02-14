from django.shortcuts import render
from core.forms import NewContactForm
from kca_project.votd import get_votd
from events.utils import get_upcoming_occurrences
from datetime import datetime, timedelta
from django.utils import timezone

def index(request):
    votd_data = get_votd()
    context = {}

    # Get upcoming events for the next 60 days
    upcoming_occurrences = get_upcoming_occurrences(days_ahead=60, limit=3)

    # Split events for display (events1 for sidebar)
    context['events1'] = upcoming_occurrences[:2] if len(upcoming_occurrences) >= 2 else upcoming_occurrences

    if votd_data:
        context.update({
            'passage': votd_data['verse']['details']['text'],
            'reference': votd_data['verse']['details']['reference'],
            'version': votd_data['verse']['details']['version'],
        })
    return render(request, 'core/index.html', context)

def contact(request):
    if request.method == 'POST':
        form = NewContactForm(request.POST)
        if form.is_valid():
            # Contact form submitted successfully (email sending removed)
            return render(request, 'core/contact.html', {'form': NewContactForm(), 'success': True})
        return render(request, 'core/contact.html', {'form': form})
    form = NewContactForm()
    return render(request, 'core/contact.html', {'form': form})

def about(request):
    return render(request, 'core/about.html')

def giving(request):
    return render(request, 'core/giving.html')
