# Generated by Django 5.2 on 2025-05-05 17:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mymodel",
            name="updated_at",
        ),
    ]
