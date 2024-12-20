# Generated by Django 5.1.3 on 2024-12-02 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('peraturan', '0004_peraturan_id_tracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='peraturan',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('final', 'Final'), ('revised', 'Revised')], default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='peraturan',
            name='status_produk',
            field=models.CharField(max_length=50),
        ),
    ]
