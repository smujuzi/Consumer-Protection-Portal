# Generated by Django 3.0.6 on 2020-06-08 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protect', '0003_faq_faqcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faq',
            name='question',
            field=models.CharField(max_length=1000),
        ),
    ]
