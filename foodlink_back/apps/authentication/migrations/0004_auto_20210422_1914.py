# Generated by Django 3.1.5 on 2021-04-22 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20210422_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpin',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pin_code', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('ONLINE', 'ONLINE'), ('CASH', 'CASH')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment_method', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]