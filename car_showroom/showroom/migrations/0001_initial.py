# Generated by Django 4.2.3 on 2023-08-04 10:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("car", "0001_initial"),
        ("provider", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Showroom",
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
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=50)),
                (
                    "location",
                    django_countries.fields.CountryField(default="US", max_length=2),
                ),
                (
                    "balance",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "discount_percent",
                    models.PositiveSmallIntegerField(
                        default=5,
                        validators=[django.core.validators.MaxValueValidator(100)],
                    ),
                ),
                ("quantity_for_discount", models.PositiveSmallIntegerField(default=10)),
            ],
            options={
                "verbose_name": "Showroom",
                "verbose_name_plural": "Showrooms",
                "db_table": "showrooms",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="ShowroomPurchase",
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
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("quantity", models.PositiveSmallIntegerField(default=0)),
                ("amount", models.PositiveIntegerField(default=0)),
                (
                    "model",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="car.carmodel",
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="provider.provider",
                    ),
                ),
                (
                    "showroom",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="showroom.showroom",
                    ),
                ),
            ],
            options={
                "verbose_name": "SR_Purchase",
                "verbose_name_plural": "SR_Purchases",
                "db_table": "sr_purchases",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="ShowroomDiscount",
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
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("start_at", models.DateTimeField()),
                ("end_at", models.DateTimeField()),
                ("name", models.CharField(max_length=50)),
                ("description", models.CharField(max_length=255)),
                (
                    "percent",
                    models.PositiveSmallIntegerField(
                        default=5,
                        validators=[django.core.validators.MaxValueValidator(100)],
                    ),
                ),
                ("model_list", models.ManyToManyField(to="car.carmodel")),
                (
                    "showroom",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="showroom.showroom",
                    ),
                ),
            ],
            options={
                "verbose_name": "SR_Discount",
                "verbose_name_plural": "SR_Discounts",
                "db_table": "sr_discounts",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="ShowroomCarCharacteristics",
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
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "brand",
                    models.CharField(
                        choices=[
                            ("Toyota", "Toyota"),
                            ("Honda", "Honda"),
                            ("Ford", "Ford"),
                            ("BMW", "BMW"),
                            ("Mercedes-Benz", "Mercedes-Benz"),
                            ("Audi", "Audi"),
                            ("Chevrolet", "Chevrolet"),
                            ("Volkswagen", "Volkswagen"),
                            ("Hyundai", "Hyundai"),
                            ("Nissan", "Nissan"),
                            ("Kia", "Kia"),
                            ("Volvo", "Volvo"),
                            ("Subaru", "Subaru"),
                            ("Mazda", "Mazda"),
                            ("Lexus", "Lexus"),
                            ("Tesla", "Tesla"),
                            ("Porsche", "Porsche"),
                            ("Jeep", "Jeep"),
                            ("Land Rover", "Land Rover"),
                            ("Ferrari", "Ferrari"),
                            ("Lamborghini", "Lamborghini"),
                            ("Maserati", "Maserati"),
                            ("Bentley", "Bentley"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "fuel",
                    models.CharField(
                        choices=[
                            ("Petrol", "Petrol"),
                            ("Diesel", "Diesel"),
                            ("Biodiesel", "Biodiesel"),
                            ("Propane", "Propane"),
                            ("Electricity", "Electricity"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "transmission",
                    models.CharField(
                        choices=[
                            ("Mechanical", "Mechanical"),
                            ("Automatic", "Automatic"),
                            ("Variator", "Variator"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "showroom",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="showroom.showroom",
                    ),
                ),
            ],
            options={
                "verbose_name": "SR_Charact",
                "verbose_name_plural": "SR_Characts",
                "db_table": "sr_car_charact",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="ShowroomCar",
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
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "showroom_price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("quantity", models.PositiveSmallIntegerField(default=0)),
                (
                    "model",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="car.carmodel",
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="provider.provider",
                    ),
                ),
                (
                    "showroom",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.RESTRICT,
                        to="showroom.showroom",
                    ),
                ),
            ],
            options={
                "verbose_name": "SR_Car",
                "verbose_name_plural": "SR_Cars",
                "db_table": "sr_car",
                "ordering": ["-updated_at"],
            },
        ),
        migrations.AddField(
            model_name="showroom",
            name="model_list",
            field=models.ManyToManyField(
                through="showroom.ShowroomCar", to="car.carmodel"
            ),
        ),
    ]
