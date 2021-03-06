# Generated by Django 3.0.8 on 2020-11-16 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lop', '0002_auto_20201116_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(default=None, max_length=2000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='dateclosed',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='dateopened',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(default=None, max_length=1000),
            preserve_default=False,
        ),
    ]
