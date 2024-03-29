# Generated by Django 2.1.8 on 2019-09-18 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('ProductId', models.AutoField(primary_key=True, serialize=False)),
                ('ProductName', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'GN_Product',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceCall',
            fields=[
                ('CallTypeId', models.AutoField(primary_key=True, serialize=False)),
                ('CallTypeDetails', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'GN_ServiceCall',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceCategory',
            fields=[
                ('CategoryId', models.AutoField(primary_key=True, serialize=False)),
                ('CategoryDetails', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'GN_ServiceCategory',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceDetails',
            fields=[
                ('ServiceDetailsId', models.AutoField(primary_key=True, serialize=False)),
                ('CustomerName', models.CharField(max_length=100)),
                ('Mobile', models.CharField(max_length=20)),
                ('TractorPurchaseDate', models.DateTimeField()),
                ('HoursProvided', models.IntegerField()),
                ('DateOfInstallation', models.DateTimeField()),
                ('ServiceDemandDate', models.DateTimeField()),
                ('ServiceStartDate', models.DateTimeField()),
                ('ServiceEndDate', models.DateTimeField()),
                ('ServiceIncome', models.FloatField()),
                ('VisitDate', models.DateTimeField()),
                ('MobileCreatedDT', models.DateTimeField()),
                ('MobileEditedDT', models.DateTimeField()),
                ('MobileLogCount', models.IntegerField()),
                ('MobileId', models.IntegerField()),
                ('ServerInsertDateTime', models.DateTimeField(auto_now_add=True)),
                ('ServerUpdateDateTime', models.DateTimeField(auto_now=True)),
                ('IsVerify', models.BooleanField(db_column='IsVerify', default=False)),
            ],
            options={
                'db_table': 'GN_ServiceDetails',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('UserId', models.AutoField(primary_key=True, serialize=False)),
                ('UserName', models.CharField(max_length=50)),
                ('Password', models.CharField(max_length=50)),
                ('IsActive', models.IntegerField(db_column='IsActive', default=1)),
            ],
            options={
                'db_table': 'GN_UserInfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('Id', models.AutoField(db_column='AreaId', primary_key=True, serialize=False)),
                ('AreaName', models.CharField(db_column='AreaName', max_length=100, unique=True)),
            ],
            options={
                'db_table': 'Area',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MotorTechnician',
            fields=[
                ('Id', models.AutoField(db_column='TechnicianId', primary_key=True, serialize=False)),
                ('Name', models.CharField(db_column='TechnicianName', default='', max_length=100)),
                ('Designation', models.CharField(db_column='Designation', max_length=100)),
                ('StaffId', models.CharField(db_column='StaffId', default='', max_length=100, unique=True)),
                ('MobileNo', models.CharField(db_column='MobileNo', default='', max_length=20)),
                ('BloodGroup', models.CharField(db_column='BloodGroup', max_length=20)),
                ('Notes', models.CharField(db_column='Notes', max_length=100)),
            ],
            options={
                'db_table': 'MotorTechnician',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('Id', models.AutoField(db_column='TargetId', primary_key=True, serialize=False)),
                ('WarrantyService', models.IntegerField(db_column='WarrantyService', default=0)),
                ('PostWarrantyService', models.IntegerField(db_column='PostWarrantyService', default=0)),
                ('Notes', models.CharField(db_column='Notes', max_length=100)),
                ('EntryDate', models.DateTimeField(auto_now_add=True, db_column='EntryDate')),
                ('TechnicianCode', models.ForeignKey(db_column='TsaTsoStaffID', on_delete=django.db.models.deletion.CASCADE, to='MotorServicesApp.MotorTechnician')),
            ],
            options={
                'db_table': 'Target',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Territory',
            fields=[
                ('Id', models.AutoField(db_column='TerritoryId', primary_key=True, serialize=False)),
                ('Name', models.CharField(db_column='TerritoryName', max_length=100)),
                ('Code', models.CharField(db_column='TerritoryCode', max_length=50)),
                ('Notes', models.CharField(db_column='Notes', max_length=100)),
                ('user', models.ForeignKey(db_column='EntryBy', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Territory',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='target',
            name='TerritoryId',
            field=models.ForeignKey(db_column='TerritoryId', on_delete=django.db.models.deletion.CASCADE, to='MotorServicesApp.Territory'),
        ),
        migrations.AddField(
            model_name='target',
            name='user',
            field=models.ForeignKey(db_column='SupervisorCode', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='motortechnician',
            name='TerritoryCode',
            field=models.ForeignKey(db_column='TerritoryCode', on_delete=django.db.models.deletion.CASCADE, to='MotorServicesApp.Territory'),
        ),
        migrations.AddField(
            model_name='motortechnician',
            name='user',
            field=models.ForeignKey(db_column='SupervisorCode', default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
