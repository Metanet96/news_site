# Generated by Django 3.1 on 2020-08-11 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0003_post_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='is_deleted',
        ),
    ]
