# Generated by Django 2.1.1 on 2019-11-22 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogging', '0003_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]
