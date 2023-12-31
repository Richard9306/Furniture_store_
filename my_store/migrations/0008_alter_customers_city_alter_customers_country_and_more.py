# Generated by Django 4.2.2 on 2023-08-21 14:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("my_store", "0007_alter_customers_birth_date_alter_customers_city_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customers",
            name="city",
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
        migrations.AlterField(
            model_name="customers",
            name="country",
            field=models.CharField(
                blank=True, default="Polska", max_length=60, null=True
            ),
        ),
        migrations.AlterField(
            model_name="customers",
            name="house_nr",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="customers",
            name="phone_nr",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name="customers",
            name="postal_code",
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name="customers",
            name="street",
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
    ]
