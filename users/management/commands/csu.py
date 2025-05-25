from django.core.management import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    def handle(self, *args, **options):
        user=CustomUser.objects.create(email="o.v.fedorova07@gmail.com")
        user.set_password("1234")
        user.is_activ = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
