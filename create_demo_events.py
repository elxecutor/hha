#!/usr/bin/env python
import os
import sys
import django
from datetime import time, date
import recurrence

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kca_project.settings')
django.setup()

from events.models import Event
from recurrence import Recurrence

def create_demo_events():
    # Clear existing events
    Event.objects.all().delete()

    # Create weekly Sunday service
    sunday_service = Event.objects.create(
        name='Sunday Worship Service',
        description='Join us for our weekly worship service where we come together to praise God, hear His word, and fellowship with one another.',
        start_date=date(2026, 2, 9),  # Today
        start_time=time(10, 0),
        end_time=time(12, 0),
        location='Main Sanctuary',
        recurrence=Recurrence(rrules=[recurrence.Rule(freq=recurrence.WEEKLY, byday=[recurrence.SU])])
    )

    # Create one-time special event
    special_event = Event.objects.create(
        name='Community Outreach Day',
        description='A special day dedicated to serving our community through various outreach programs and activities.',
        start_date=date(2026, 3, 15),
        start_time=time(9, 0),
        end_time=time(15, 0),
        location='Community Center',
        is_special=True,
        speakers='Pastor John, Community Leaders',
        hashtags='#Outreach #Community #Service'
    )

    # Create monthly prayer meeting
    prayer_meeting = Event.objects.create(
        name='Monthly Prayer Meeting',
        description='Come join us for our monthly prayer meeting where we lift up our community, nation, and world in prayer.',
        start_date=date(2026, 2, 15),
        start_time=time(19, 0),
        end_time=time(20, 30),
        location='Fellowship Hall',
        recurrence=Recurrence(rrules=[recurrence.Rule(freq=recurrence.MONTHLY, bymonthday=15)])
    )

    # Create annual Christmas event
    christmas_event = Event.objects.create(
        name='Christmas Celebration',
        description='Celebrate the birth of Jesus Christ with carols, readings, and fellowship. A joyous time for the whole family.',
        start_date=date(2026, 12, 25),
        start_time=time(18, 0),
        end_time=time(21, 0),
        location='Main Sanctuary',
        is_special=True,
        recurrence=Recurrence(rrules=[recurrence.Rule(freq=recurrence.YEARLY, bymonth=12, bymonthday=25)]),
        speakers='Pastor John, Choir',
        hashtags='#Christmas #Jesus #Celebration'
    )

    # Create youth event
    youth_event = Event.objects.create(
        name='Youth Bible Study',
        description='Weekly Bible study session for our youth group. Learn, grow, and connect with peers in faith.',
        start_date=date(2026, 2, 11),  # Next Tuesday
        start_time=time(18, 30),
        end_time=time(20, 0),
        location='Youth Room',
        recurrence=Recurrence(rrules=[recurrence.Rule(freq=recurrence.WEEKLY, byday=[recurrence.TU])])
    )

    print('Demo events created successfully!')
    print(f'Total events: {Event.objects.count()}')

    # Show created events
    for event in Event.objects.all():
        recurrence_info = "Recurring" if event.recurrence else "One-time"
        print(f"- {event.name} ({recurrence_info}) - {event.location}")

if __name__ == '__main__':
    create_demo_events()