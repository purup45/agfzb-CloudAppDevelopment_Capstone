# Generated by Django 3.2.15 on 2022-09-25 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarMake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('type_ch', models.CharField(choices=[('BMW', 'BMW'), ('Benz', 'Benz'), ('Swift', 'Swift')], max_length=10)),
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('year', models.DateField()),
                ('car_make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangoapp.carmake')),
            ],
        ),
    ]