# blog/migrations/0002_create_content_manager_group.py
from django.db import migrations
from django.contrib.auth.models import Group, Permission

def create_group(apps, schema_editor):
    content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
    if created:
        # Получаем права для модели Post
        permissions = Permission.objects.filter(
            codename__in=('add_post', 'change_post', 'delete_post')
        )
        content_manager_group.permissions.add(*permissions)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_group),
    ]