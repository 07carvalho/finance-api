# Generated by Django 3.2.7 on 2021-09-02 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('deleted_at', models.DateTimeField(blank=True, default=None, null=True)),
                ('name', models.CharField(max_length=120)),
                ('type', models.CharField(choices=[('bank', 'Bank Account'), ('cash', 'Cash')], default='bank', max_length=4)),
                ('bank', models.CharField(blank=True, max_length=120, null=True)),
                ('income', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('expense', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=9)),
                ('last_update', models.DateTimeField(null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_filed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
            managers=[
                ('activated', django.db.models.manager.Manager()),
            ],
        ),
    ]
