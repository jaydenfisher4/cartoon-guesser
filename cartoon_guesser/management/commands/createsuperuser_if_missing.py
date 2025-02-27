import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Creates a superuser if none exists"

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.getenv("ADMIN_USERNAME", "beee")  
        email = os.getenv("ADMIN_EMAIL", "jaydenfisher46176@gmail.com")
        password = os.getenv("ADMIN_PASSWORD", "Catfish1.") 

        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created successfully"))
        else:
            self.stdout.write(self.style.SUCCESS("Superuser already exists"))