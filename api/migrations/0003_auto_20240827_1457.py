# Generated by Django 3.0.7 on 2024-08-27 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_is_staff'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vente',
            name='reference',
            field=models.CharField(default=0, max_length=250),
            preserve_default=False,
        ),
    ]
