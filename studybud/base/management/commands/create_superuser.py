import os
from django.core.management.base import BaseCommand, CommandError
from base.models import User

class Command(BaseCommand):
    help = 'Creates a superuser account'

    def handle(self, *args, **options):        

        # Get the superuser credentials from environment variables
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not username or not email or not password:
            raise CommandError('Username, email, and password are required. Please set the necessary environment variables.')        
        if not User.objects.filter(username=username, email=email).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS('Superuser account created successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Superuser account already exists.'))