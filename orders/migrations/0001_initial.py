# Generated manually for reconstructed baseline
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('external_id', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='products.product')),
            ],
        ),
    ]
