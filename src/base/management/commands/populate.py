import faker
from django.conf import settings
from django.core.management.base import BaseCommand

from account.models import User


class Command(BaseCommand):
    help = "Populate the database with dummy data"

    def handle(self, *args, **options):
        if not settings.DEBUG:
            self.stdout.write("This command can only be run in DEBUG mode")
            return

        self.fake = faker.Faker()
        self.populate_users()

    def populate_users(self):
        users = []
        for _ in range(100):
            users.append(User(full_name=self.fake.name(), email=self.fake.email(), password=self.fake.password()))

        User.objects.filter(is_superuser=False).delete()
        User.objects.bulk_create(users)
        self.stdout.write("Users created successfully")
