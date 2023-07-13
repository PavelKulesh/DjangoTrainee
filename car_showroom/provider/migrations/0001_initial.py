# Generated by Django 4.2.3 on 2023-07-13 11:54

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProviderCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('provider_price', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='common.carmodel')),
            ],
            options={
                'verbose_name': 'Provider_Car',
                'verbose_name_plural': 'Provider_Cars',
                'db_table': 'provider_cars',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ProviderModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('foundation_year', models.PositiveSmallIntegerField(default=2010)),
                ('showroom_quantity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('balance', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('discount_percent', models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MaxValueValidator(100)])),
                ('quantity_for_discount', models.PositiveSmallIntegerField(default=20)),
                ('car_list', models.ManyToManyField(through='provider.ProviderCar', to='common.carmodel')),
            ],
            options={
                'verbose_name': 'Provider',
                'verbose_name_plural': 'Providers',
                'db_table': 'providers',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='ProviderDiscount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=255)),
                ('percent', models.PositiveSmallIntegerField(default=5, validators=[django.core.validators.MaxValueValidator(100)])),
                ('car_list', models.ManyToManyField(to='common.carmodel')),
                ('provider', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='provider.providermodel')),
            ],
            options={
                'verbose_name': 'Provider_Discount',
                'verbose_name_plural': 'Provider_Discounts',
                'db_table': 'provider_discounts',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.AddField(
            model_name='providercar',
            name='provider',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='provider.providermodel'),
        ),
    ]