# Generated by Django 2.0.10 on 2021-05-11 06:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('circles', '0005_invitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='used_by',
            field=models.ForeignKey(help_text='User that used the code to enter the circle', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
