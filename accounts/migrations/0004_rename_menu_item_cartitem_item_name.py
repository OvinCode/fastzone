# Generated by Django 5.0.4 on 2024-04-28 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_cartitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='menu_item',
            new_name='item_name',
        ),
    ]
