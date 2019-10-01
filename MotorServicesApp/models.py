from django.db import models
from django.forms import forms
# Create your models here.


from django.contrib.auth.models import Group, User
from django.contrib.auth.models import AbstractUser
from smart_selects.db_fields import ChainedForeignKey

class EngWiseReport(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    EngWiseReportLink = models.CharField(max_length=255, db_column='EngWiseReportLink')
    EngId = models.ForeignKey(User, db_column='UserId', on_delete=models.CASCADE, default=2)

    def __str__(self):
        return self.EngWiseReportLink

    class Meta:
        verbose_name_plural = 'TSA/TSO-Report'
        managed = False
        db_table = 'EngWiseReport'

class Area(models.Model):
    Id = models.AutoField(primary_key=True, db_column='AreaId')
    AreaName = models.CharField(max_length=100, db_column='AreaName',unique=True)
    Notes = models.CharField(max_length=100, db_column='Notes',default='')

    # RegionId = models.ForeignKey(Region, db_column='RegionId', on_delete=models.CASCADE)
    #user = models.ForeignKey(User)

    def __str__(self):
        return self.AreaName

    class Meta:
        managed = False
        db_table = 'Area'

class UserArea(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    UserId = models.ForeignKey(User,db_column='UserId',on_delete=models.CASCADE)
    AreaId = models.ManyToManyField(Area, db_column='AreaId')

    # def __str__(self):
    #     return self.UserId

    class Meta:
        managed = False
        db_table = 'UserArea'

class Territory(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TerritoryId')
    Name = models.CharField(max_length=100, db_column='TerritoryName')
    Code = models.CharField(max_length=50, db_column='TerritoryCode')
    Notes = models.CharField(max_length=100, db_column='Notes')
    AreaId = models.ForeignKey(Area, db_column='AreaId', on_delete=models.CASCADE,verbose_name='Area')
    user = models.ForeignKey(User,db_column='EntryBy',on_delete=models.CASCADE)

    def __str__(self):
        #print("====="+self.Name)
        return self.Name

    class Meta:
        managed = False
        db_table = 'Territory'

class MotorTechnician(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TechnicianId')
    Name = models.CharField(max_length=100, db_column='TechnicianName', default='')
    Designation = models.CharField(max_length=100, db_column='Designation')
    StaffId = models.CharField(max_length=100, db_column='StaffId', default='',unique=True)
    TerritoryCode = models.ForeignKey(Territory, db_column='TerritoryCode', on_delete=models.CASCADE)
    MobileNo = models.CharField(max_length=20, db_column='MobileNo', default='')
    BloodGroup = models.CharField(max_length=20, db_column='BloodGroup')
    Notes = models.CharField(max_length=100, db_column='Notes')
    user = models.ForeignKey(User, db_column='SupervisorCode', on_delete=models.CASCADE, default=1)

    #added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name_plural = 'Motor Technician'
        managed = False
        db_table = 'MotorTechnician'

class Target(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TargetId')
    TechnicianCode = models.ForeignKey(MotorTechnician, db_column='TsaTsoStaffID', on_delete=models.CASCADE)
    TerritoryId = models.ForeignKey(Territory, db_column='TerritoryId', on_delete=models.CASCADE)
    WarrantyService = models.IntegerField(db_column='WarrantyService', default=0)
    PostWarrantyService = models.IntegerField(db_column='PostWarrantyService', default=0)
    Notes = models.CharField(max_length=100, db_column='Notes')
    EntryDate = models.DateTimeField(auto_now_add=True, db_column='EntryDate')
    user = models.ForeignKey(User, db_column='SupervisorCode', on_delete=models.CASCADE)

    def __str__(self):
        return self.TechnicianCode.Name

    class Meta:
        managed = False
        db_table = 'Target'



class UserInfo(models.Model):
    UserId = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    IsActive = models.IntegerField(default=1, db_column='IsActive')
    user = models.ForeignKey(User, db_column='SupervisorID', on_delete=models.CASCADE)
    MotorTechnicianId = models.ForeignKey(MotorTechnician, db_column='MotorTechnicianId', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.UserName

    class Meta:
        managed = False
        db_table = 'GN_UserInfo'

    # def __str__(self):
    #     return '{}, {}'.format(self.UserName, self.Password)

class ServiceCategory(models.Model):
    CategoryId = models.AutoField(primary_key=True)
    CategoryDetails = models.CharField(max_length=50)

    def __str__(self):
        return self.CategoryDetails

    class Meta:
        managed = False
        db_table = 'GN_ServiceCategory'

    # def __str__(self):
    #     return '{}, {}'.format(self.CategoryDetails)

class Product(models.Model):
    ProductId = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=50)

    def __str__(self):
        return self.ProductName

    class Meta:
        managed = False
        db_table = 'GN_Product'

    # def __str__(self):
    #     return '{}, {}'.format(self.ProductName)


class ServiceCall(models.Model):
    CallTypeId = models.AutoField(primary_key=True)
    CallTypeDetails = models.CharField(max_length=50)

    def __str__(self):
        return self.CallTypeDetails

    class Meta:
        managed = False
        db_table = 'GN_ServiceCall'

#17613
class ServiceDetails(models.Model):
    ServiceDetailsId = models.AutoField(primary_key=True)
    CustomerName = models.CharField(max_length=100)
    Mobile = models.CharField(max_length=20)
    TractorPurchaseDate = models.DateTimeField()
    HoursProvided = models.IntegerField()
    DateOfInstallation = models.DateTimeField()
    ServiceDemandDate = models.DateTimeField()
    ServiceStartDate = models.DateTimeField()
    ServiceEndDate = models.DateTimeField()
    ServiceIncome = models.FloatField()
    VisitDate = models.DateTimeField()
    MobileCreatedDT = models.DateTimeField()
    MobileEditedDT = models.DateTimeField()
    MobileLogCount = models.IntegerField()
    MobileId = models.IntegerField()
    ServerInsertDateTime = models.DateTimeField(auto_now_add=True)
    ServerUpdateDateTime = models.DateTimeField(auto_now=True)

    #IsVerify = models.BooleanField(db_column='IsVerify', default=False)
    IsVerify = models.IntegerField(db_column='IsVerify', default=0)

    #UserId = models.ForeignKey(UserInfo, db_column='UserId', on_delete=models.CASCADE)
    UserId = models.ForeignKey(UserInfo, db_column='UserId', on_delete=models.CASCADE)
    CategoryId = models.ForeignKey(ServiceCategory, db_column='CategoryId', on_delete=models.CASCADE)
    ProductId = models.ForeignKey(Product, db_column='ProductId', on_delete=models.CASCADE)
    CallTypeId = models.ForeignKey(ServiceCall, db_column='CallTypeId', on_delete=models.CASCADE)
    SupervisorCode = models.ForeignKey(User, db_column='SupervisorCode', on_delete=models.CASCADE)

    def __str__(self):
        return self.CustomerName

    class Meta:
        verbose_name_plural = 'Service Details'
        managed = False
        db_table = 'GN_ServiceDetails'



class CSIInfo(models.Model):
    CSIINforId = models.AutoField(primary_key=True)
    AreaId = models.ForeignKey(Area, db_column='AreaId', on_delete=models.CASCADE)
    #TerritoryId = models.ForeignKey(Territory, db_column='TerritoryId', on_delete=models.CASCADE)

    TerritoryId = ChainedForeignKey(
        Territory,
        chained_field="AreaId",
        chained_model_field="AreaId",
        show_all=False,
        auto_choose=True,
        sort=True,
        db_column='TerritoryId'
    )

    CSIValue = models.DecimalField(db_column='CSIValue', decimal_places=2, max_digits=10)

    def __str__(self):
        return str("CSI Info Added for "+self.TerritoryId.Name+" and value is "+ str(self.CSIValue))

    class Meta:
        verbose_name_plural = 'CSI Info'
        managed = False
        db_table = 'CSIInfo'


class SixHourInfo(models.Model):
    SixHourInfoId = models.AutoField(primary_key=True)
    AreaId = models.ForeignKey(Area, db_column='AreaId', on_delete=models.CASCADE)
    TerritoryId = ChainedForeignKey(
        Territory,
        chained_field="AreaId",
        chained_model_field="AreaId",
        show_all=False,
        auto_choose=True,
        sort=True,
        db_column='TerritoryId'
    )
    SixHourValue = models.DecimalField(decimal_places=2, max_digits=10, db_column='SixHourValue')

    def __str__(self):
        return str("Six Hour Added for "+self.TerritoryId.Name+" and value is "+ str(self.SixHourValue))

    class Meta:
        verbose_name_plural = 'Six Hour'
        managed = False
        db_table = 'SixHourInfo'