# Generated by Django 4.2.2 on 2023-06-12 10:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0005_rating"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tour",
            name="description",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
