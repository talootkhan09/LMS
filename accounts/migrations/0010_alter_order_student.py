# Generated by Django 3.2.5 on 2022-05-17 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20220513_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='accounts.student'),
        ),
    ]
