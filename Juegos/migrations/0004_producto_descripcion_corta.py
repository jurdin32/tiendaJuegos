# Generated by Django 4.1 on 2022-08-23 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Juegos', '0003_producto_precio'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='descripcion_corta',
            field=models.TextField(blank=True, null=True),
        ),
    ]