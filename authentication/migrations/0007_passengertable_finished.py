# Generated by Django 5.0.4 on 2024-06-02 13:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authentication", "0006_publishertable_finished"),
    ]

    operations = [
        migrations.AddField(
            model_name="passengertable",
            name="finished",
            field=models.BooleanField(default=False),
        ),
    ]
