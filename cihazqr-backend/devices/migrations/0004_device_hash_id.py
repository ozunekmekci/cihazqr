from django.db import migrations, models
import hashlib


def gen_hash_id(device):
    base = f"{device.name or ''}{device.serial or ''}{device.brand or ''}{device.model or ''}"
    if not base:
        base = str(device.created_at)
    hash_val = hashlib.sha256(base.encode()).hexdigest()[:10]
    return hash_val

def fill_hash_ids(apps, schema_editor):
    Device = apps.get_model('devices', 'Device')
    used_hashes = set()
    for device in Device.objects.all():
        hash_id = gen_hash_id(device)
        # Çakışma varsa id'nin son 2 hanesini ekle
        original_hash = hash_id
        suffix = str(device.id)[-2:]
        while hash_id in used_hashes or Device.objects.filter(hash_id=hash_id).exclude(id=device.id).exists():
            hash_id = (original_hash[:-2] + suffix).zfill(10)
        device.hash_id = hash_id
        device.save()
        used_hashes.add(hash_id)

class Migration(migrations.Migration):
    dependencies = [
        ('devices', '0003_devicedocument_devicenote'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='hash_id',
            field=models.CharField(max_length=10, null=True, blank=True),
        ),
        migrations.RunPython(fill_hash_ids, reverse_code=migrations.RunPython.noop),
    ] 