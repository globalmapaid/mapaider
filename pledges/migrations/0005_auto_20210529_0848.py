# Generated by Django 3.2 on 2021-05-29 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pledges', '0004_auto_20210524_2005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pledge',
            options={'verbose_name': 'Pledge', 'verbose_name_plural': 'Pledges'},
        ),
        migrations.RemoveField(
            model_name='pledge',
            name='address',
        ),
        migrations.AddField(
            model_name='pledge',
            name='city',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='pledge',
            name='notes',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='pledge',
            name='street',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='geom_type',
            field=models.CharField(blank=True, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='pledge',
            name='measurement_unit',
            field=models.CharField(choices=[('m2', 'm2'), ('acres', 'Acres'), ('ha', 'Hectares')], default='ha', max_length=6),
        ),
    ]