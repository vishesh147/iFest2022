# Generated by Django 4.0.4 on 2022-10-16 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ifest2022', '0005_profile_gold'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='amount',
            field=models.IntegerField(null=True),
        ),
    ]