# Generated by Django 3.2.5 on 2021-07-04 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_statsprojection_lng_eq'),
    ]

    operations = [
        migrations.AddField(
            model_name='statsevent',
            name='fname',
            field=models.CharField(default='', max_length=255),
        ),
    ]
