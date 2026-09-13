from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import Task

class Command(BaseCommand):
    help = "Create a demo user and sample tasks."
    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(username="demo", defaults={"email": "demo@example.com"})
        if created: user.set_password("DemoPass123!"); user.save()
        Task.objects.get_or_create(owner=user, title="Learn Django APIs", defaults={"description": "Practice JWT, middleware, signals and commands."})
        self.stdout.write(self.style.SUCCESS("Demo data is ready. Login: demo / DemoPass123!"))

