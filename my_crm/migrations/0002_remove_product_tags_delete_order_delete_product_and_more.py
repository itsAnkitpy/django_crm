# Generated by Django 4.1.3 on 2022-11-22 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_crm', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
