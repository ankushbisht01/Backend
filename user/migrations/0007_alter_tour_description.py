# Generated by Django 4.2.2 on 2023-06-12 10:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0006_alter_tour_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tour",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
