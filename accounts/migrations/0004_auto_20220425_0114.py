# Generated by Django 3.2.5 on 2022-04-24 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_book_order_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.book'),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Borrow', 'Borrow'), ('Return', 'Return')], max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.student'),
        ),
    ]
