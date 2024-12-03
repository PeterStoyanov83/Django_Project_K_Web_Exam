from django.core.management.base import BaseCommand
from django.db import connection
from django.apps import apps
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Cleans the database by deleting all data from all tables except superusers'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting database cleanup...'))

        # Get all models
        models = apps.get_models()

        with connection.cursor() as cursor:
            # Disable foreign key checks
            if connection.vendor == 'mysql':
                cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
            elif connection.vendor == 'sqlite':
                cursor.execute('PRAGMA foreign_keys = OFF;')
            elif connection.vendor == 'postgresql':
                cursor.execute('SET CONSTRAINTS ALL DEFERRED;')

            # Delete all data from each model, except superusers
            for model in models:
                if not model._meta.managed or model._meta.proxy:
                    continue
                if model == get_user_model():
                    self.stdout.write(f'Preserving superusers and deleting other users...')
                    model.objects.filter(is_superuser=False).delete()
                else:
                    self.stdout.write(f'Cleaning {model._meta.verbose_name_plural}...')
                    model.objects.all().delete()

            # Re-enable foreign key checks
            if connection.vendor == 'mysql':
                cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')
            elif connection.vendor == 'sqlite':
                cursor.execute('PRAGMA foreign_keys = ON;')
            elif connection.vendor == 'postgresql':
                cursor.execute('SET CONSTRAINTS ALL IMMEDIATE;')

        self.stdout.write(self.style.SUCCESS('Database cleanup completed successfully!'))
