# Generated by Django 3.0.6 on 2020-06-03 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20200603_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='role',
            field=models.CharField(choices=[('1', 'complainant'), ('2', 'admin'), ('3', 'I.T. Officer'), ('4', 'Service Desk'), ('5', 'Director Legal')], default='complainant', max_length=200),
        ),
    ]
