# Generated by Django 3.1 on 2020-08-07 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='time',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]