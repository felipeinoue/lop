# Generated by Django 3.0.8 on 2020-11-18 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lop', '0007_auto_20201117_0823'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='weeklyemail',
            field=models.BooleanField(default=False),
        ),
    ]