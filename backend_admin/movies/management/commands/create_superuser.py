import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crate a superuser"

    def handle(self, *args, **options):
        password = os.getenv("SUPERUSER_PASS", "@J2JqrPRYoFnVv2jvV")
        username = os.getenv("SUPERUSER_NAME", "admin")
        if User.objects.filter(username=username).exists():
            return

        User.objects.create_superuser(username, "admin@example.com", password)
