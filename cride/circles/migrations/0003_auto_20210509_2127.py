# Generated by Django 2.0.10 on 2021-05-09 21:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0002_auto_20210509_1641'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='remainig_invitation',
            new_name='remainig_invitations',
        ),
    ]