# Generated by Django 3.2.12 on 2022-04-20 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('price',)},
        ),
    ]
