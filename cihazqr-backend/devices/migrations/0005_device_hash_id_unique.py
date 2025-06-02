from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('devices', '0004_device_hash_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='hash_id',
            field=models.CharField(max_length=10, unique=True, blank=True),
        ),
    ] 