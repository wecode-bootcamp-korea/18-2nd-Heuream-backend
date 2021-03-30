# Generated by Django 3.1.7 on 2021-03-31 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_brandimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image_url',
            field=models.URLField(default=None, max_length=2000),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='BrandImage',
        ),
    ]
