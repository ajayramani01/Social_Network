# Generated by Django 4.2.13 on 2024-06-13 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("social_network", "0002_follow_user_followers"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="password",
            field=models.CharField(blank=True, max_length=500),
        ),
    ]