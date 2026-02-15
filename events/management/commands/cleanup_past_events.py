from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from events.models import Event


class Command(BaseCommand):
    help = 'Delete past events that have no future occurrences'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        now = timezone.now()
        today = now.date()
        
        # Get all events
        events = Event.objects.all()
        deleted_count = 0
        
        for event in events:
            should_delete = False
            
            if event.recurrence:
                # For recurring events, check if there are any future occurrences
                future_occurrences = event.get_occurrences(now, now + timedelta(days=365*2))
                if not future_occurrences:
                    should_delete = True
                    reason = "recurring event with no future occurrences"
            else:
                # For one-time events, check if start_date is in the past
                if event.start_date < today:
                    should_delete = True
                    reason = f"one-time event with past start date ({event.start_date})"
            
            if should_delete:
                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(f'Would delete: "{event.name}" - {reason}')
                    )
                else:
                    event.delete()
                    self.stdout.write(
                        self.style.SUCCESS(f'Deleted: "{event.name}" - {reason}')
                    )
                deleted_count += 1
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'Dry run complete. Would delete {deleted_count} events.')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Cleanup complete. Deleted {deleted_count} past events.')
            )