# Generated by Django 3.1.7 on 2021-03-31 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210331_0449'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Line',
            new_name='BrandLine',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='line',
            new_name='brand_line',
        ),
        migrations.RenameField(
            model_name='subline',
            old_name='line',
            new_name='brand_line',
        ),
        migrations.AlterModelTable(
            name='brandline',
            table='brand_lines',
        ),
    ]
