# Generated by Django 5.0.3 on 2025-04-16 10:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=50)),
                ('governorate', models.CharField(max_length=50)),
                ('property_type', models.CharField(choices=[('commercial', 'تجاري')], max_length=20)),
                ('total_area', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('investors', models.ManyToManyField(blank=True, limit_choices_to={'user_type': 'investor'}, related_name='invested_properties', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(limit_choices_to={'user_type': 'owner'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_type', models.CharField(choices=[('shop', 'محل'), ('office', 'مكتب'), ('apartment', 'شقة'), ('storge', 'مخزن'), ('parking', 'موقف سيارات')], max_length=20)),
                ('unit_number', models.CharField(max_length=50)),
                ('area', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monthly_rent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_available', models.BooleanField(default=True)),
                ('features', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property')),
            ],
        ),
    ]
