import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from hymnal.models import Hymn

class Command(BaseCommand):
    help = 'Load hymns from hymns.json into the database'

    def handle(self, *args, **options):
        hymns_file = os.path.join(settings.BASE_DIR, 'hymns.json')
        
        if not os.path.exists(hymns_file):
            self.stdout.write(self.style.ERROR(f'Hymns file not found: {hymns_file}'))
            return
        
        with open(hymns_file, 'r') as f:
            hymns_data = json.load(f)
        
        for key, hymn_data in hymns_data.items():
            hymn, created = Hymn.objects.get_or_create(
                title=hymn_data['title'],
                defaults={'lyrics': '\n'.join(hymn_data['lyrics'])}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created hymn: {hymn.title}'))
            else:
                self.stdout.write(f'Hymn already exists: {hymn.title}')
        
        self.stdout.write(self.style.SUCCESS('Hymns loaded successfully'))