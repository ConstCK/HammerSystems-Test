# Generated by Django 5.1.3 on 2024-11-30 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pass_code',
            field=models.CharField(blank=True, max_length=4, null=True, verbose_name='4-значный код для входа'),
        ),
    ]
