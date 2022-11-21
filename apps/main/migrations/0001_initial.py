# Generated by Django 4.1.1 on 2022-09-27 16:55

from django.db import migrations, models
import main.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MainEntity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "datetime_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="время создания"
                    ),
                ),
                (
                    "datetime_updated",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="время обновления"
                    ),
                ),
                (
                    "datetime_deleted",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="время удаления"
                    ),
                ),
                ("first_name", models.CharField(max_length=255, verbose_name="имя")),
                ("last_name", models.CharField(max_length=255, verbose_name="фамилия")),
                (
                    "phone_number",
                    models.CharField(max_length=20, verbose_name="номер телефона"),
                ),
                (
                    "apartment_number",
                    models.IntegerField(verbose_name="номер дома/квартиры"),
                ),
                (
                    "has_paid_taxes",
                    models.BooleanField(default=True, verbose_name="оплата налогов"),
                ),
                ("email", models.EmailField(max_length=254, verbose_name="почта")),
            ],
            options={
                "verbose_name": "Юзер с квартирой",
                "verbose_name_plural": "Юзеры с квартирой",
            },
            bases=(models.Model, main.validators.TempModelValidator),
        ),
    ]
