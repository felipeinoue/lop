# Generated by Django 3.0.8 on 2020-11-16 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lop', '0005_auto_20201116_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='lop_username',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
    ]
