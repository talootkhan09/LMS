# Generated by Django 3.2.5 on 2022-05-12 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_order_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
