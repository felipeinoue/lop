# Generated by Django 3.0.8 on 2020-11-16 17:03

from django.db import migrations, models
import lop.models


class Migration(migrations.Migration):

    dependencies = [
        ('lop', '0004_auto_20201116_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='upload',
            field=models.FileField(default=None, upload_to=lop.models.user_directory_path),
            preserve_default=False,
        ),
    ]
