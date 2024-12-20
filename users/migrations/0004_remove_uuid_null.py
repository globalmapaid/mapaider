# Generated by Django 4.1.2 on 2023-02-19 23:47
import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0003_populate_uuid_values'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='uuid'),
        ),
    ]
