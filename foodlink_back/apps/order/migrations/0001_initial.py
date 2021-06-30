# Generated by Django 3.1.5 on 2021-05-12 08:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(blank=True, max_length=36, unique=True)),
                ('status', models.CharField(choices=[('COLLECTION', 'COLLECTION'), ('COOKING', 'COOKING'), ('ASSEMBLY', 'ASSEMBLY'), ('DELIVERY', 'DELIVERY')], default='COLLECTION', max_length=32)),
                ('prev_status', models.CharField(choices=[('COLLECTION', 'COLLECTION'), ('COOKING', 'COOKING'), ('ASSEMBLY', 'ASSEMBLY'), ('DELIVERY', 'DELIVERY')], default='COLLECTION', max_length=32)),
                ('total', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cook', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cook_orders', to=settings.AUTH_USER_MODEL)),
                ('delivery_address', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='core.address')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='common.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
