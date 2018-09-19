# Generated by Django 2.1.1 on 2018-09-10 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('vat', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('employees', models.IntegerField()),
                ('profit', models.BigIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interaction',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('type', models.CharField(choices=[('ad', 'advice'), ('fa', 'financial aid')], max_length=2)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Company')),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
            ],
        ),
        migrations.AddField(
            model_name='interaction',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Partner'),
        ),
    ]
