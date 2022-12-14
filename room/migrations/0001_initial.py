# Generated by Django 4.1 on 2022-10-08 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False)),
                ('capacity', models.SmallIntegerField()),
                ('numberOfBeds', models.SmallIntegerField()),
                ('roomType', models.CharField(choices=[('King', 'King'), ('Luxury', 'Luxury'), ('Normal', 'Normal'), ('Economic', 'Economic')], max_length=20)),
                ('price', models.FloatField()),
                ('statusStartDate', models.DateField(null=True)),
                ('statusEndDate', models.DateField(null=True)),
            ],
        ),
    ]
