from django.shortcuts import render
from django.core.mail import send_mail
from core.forms import NewContactForm
from kca_project.votd import get_votd
from events.models import Event
from datetime import datetime, timedelta
from django.utils import timezone

def index(request):
    votd_data = get_votd()
    context = {}

    # Get upcoming events for the next 60 days
    now = timezone.now()
    today = now.date()
    two_months_later = now + timedelta(days=60)

    # Get all events and their occurrences
    events = Event.objects.all().order_by('start_time')
    upcoming_occurrences = sorted(
        [
            {'event': event, 'date': occ.date(), 'days_until': (occ.date() - today).days}
            for event in events
            for occ in event.get_occurrences(now, two_months_later)
        ],
        key=lambda x: (x['date'], x['event'].start_time)
    )[:3]  # Show only first 3 upcoming events

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
            cleaned_data = form.cleaned_data
            name = cleaned_data['name']
            email = cleaned_data['email']
            message = cleaned_data['message']
            subject = f'Contact from {name}'
            body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
            send_mail(subject, body, email, ['contact@kca.com'])
            return render(request, 'core/contact.html', {'form': NewContactForm(), 'success': True})
        return render(request, 'core/contact.html', {'form': form})
    form = NewContactForm()
    return render(request, 'core/contact.html', {'form': form})

def giving(request):
    return render(request, 'core/giving.html')
