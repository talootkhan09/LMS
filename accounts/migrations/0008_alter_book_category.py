# Generated by Django 3.2.5 on 2022-05-11 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_student_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(max_length=200, null=True),
        ),
    ]