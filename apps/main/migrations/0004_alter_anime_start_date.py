# Generated by Django 4.1.1 on 2022-10-14 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_anime_genre"),
    ]

    operations = [
        migrations.AlterField(
            model_name="anime",
            name="start_date",
            field=models.DateTimeField(null=True, verbose_name="дата показа"),
        ),
    ]
