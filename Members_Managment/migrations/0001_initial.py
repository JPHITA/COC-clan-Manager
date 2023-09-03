# Generated by Django 4.2.2 on 2023-07-03 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('tag', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=40)),
                ('clan', models.CharField(default='', max_length=25)),
                ('role', models.CharField(default='', max_length=10)),
                ('cel', models.CharField(blank=True, max_length=20, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('current_member', models.BooleanField(default=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_updated', models.DateField(auto_now=True)),
            ],
        ),
    ]
