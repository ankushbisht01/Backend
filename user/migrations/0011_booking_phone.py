# Generated by Django 4.2.2 on 2023-06-13 18:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0010_booking"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="phone",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]