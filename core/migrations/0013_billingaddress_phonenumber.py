# Generated by Django 4.2.9 on 2024-01-22 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_billingaddress_velayat'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='phonenumber',
            field=models.CharField(default='+99365314664', max_length=12),
            preserve_default=False,
        ),
    ]