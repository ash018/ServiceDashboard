from django.db import models

# Create your models here.


from django.contrib.auth.models import Group, User


# class Region(models.Model):
#     Id = models.AutoField(primary_key=True, db_column='RegionId')
#     RegionName = models.CharField(max_length=100, db_column='RegionName')
#     PartId = models.IntegerField(db_column='PartId', default=0)
#     Notes = models.CharField(max_length=100, db_column='Notes')
#     #user = models.ForeignKey(User)
#
#     def __str__(self):
#         return self.RegionName
#
#     class Meta:
#         managed = True
#         db_table = 'Region'

class Area(models.Model):
    Id = models.AutoField(primary_key=True, db_column='AreaId')
    AreaName = models.CharField(max_length=100, db_column='AreaName',unique=True)
    Notes = models.CharField(max_length=100, db_column='Notes',default='')

    # RegionId = models.ForeignKey(Region, db_column='RegionId', on_delete=models.CASCADE)
    #user = models.ForeignKey(User)

    def __str__(self):
        return self.AreaName

    class Meta:
        managed = True
        db_table = 'Area'

class Territory(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TerritoryId')
    Name = models.CharField(max_length=100, db_column='TerritoryName')
    Code = models.CharField(max_length=50, db_column='TerritoryCode')
    Notes = models.CharField(max_length=100, db_column='Notes')
    user = models.ForeignKey(User,db_column='EntryBy',on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

    class Meta:
        managed = True
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

    # added_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.Name

    class Meta:
        managed = True
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
        managed = True
        db_table = 'Target'

class UserInfo(models.Model):
    UserId = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)
    IsActive = models.IntegerField(default=1, db_column='IsActive')
    user = models.ForeignKey(User, db_column='SupervisorID', on_delete=models.CASCADE)

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

    # def __str__(self):
    #     return '{}, {}'.format(self.CallTypeDetails)


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

    IsVerify = models.BooleanField(db_column='IsVerify', default=False)

    #UserId = models.ForeignKey(UserInfo, db_column='UserId', on_delete=models.CASCADE)
    UserId = models.ForeignKey(UserInfo, db_column='UserId', on_delete=models.CASCADE)
    CategoryId = models.ForeignKey(ServiceCategory, db_column='CategoryId', on_delete=models.CASCADE)
    ProductId = models.ForeignKey(Product, db_column='ProductId', on_delete=models.CASCADE)
    CallTypeId = models.ForeignKey(ServiceCall, db_column='CallTypeId', on_delete=models.CASCADE)
    SupervisorCode = models.ForeignKey(User, db_column='SupervisorCode', on_delete=models.CASCADE)

    def __str__(self):
        return self.CustomerName

    class Meta:
        managed = False
        db_table = 'GN_ServiceDetails'

    # def __str__(self):
    #     return '{}'.format( self.CustomerName)


# class Status(models.Model):
#     Id = models.AutoField(primary_key=True, db_column='Id')
#     Name = models.CharField(max_length=50, db_column='Name')
#
#     def __str__(self):
#         return self.Name
#
#     class Meta:
#         managed = False
#         db_table = 'Status'
#
# class AreaNew(models.Model):
#     Id = models.AutoField(primary_key=True, db_column='AreaID')
#     Name = models.CharField(max_length=100, db_column='AreaName')
#
#     def __str__(self):
#         return self.Name
#
#     class Meta:
#         managed = False
#         db_table = 'AreaNew'
#
# class UserManager(models.Model):
#     UserID = models.AutoField(primary_key=True, db_column='UserID')
#     UserName = models.CharField(max_length=255, db_column='UserName', unique=True)
#     Password = models.CharField(max_length=255, db_column='Password')
#     Status =  models.ForeignKey(Status, db_column='Status', on_delete=models.CASCADE)
#     AccessLevel = models.ForeignKey(AreaNew, db_column='AccessLevel', on_delete=models.CASCADE)
#     DisplayName = models.CharField(max_length=100, db_column='DisplayName')
#
#     def __str__(self):
#        return "Username: " + self.UserName + " has been created successfully."
#
#     def get_full_name(self):
#         return self.UserName
#
#     def get_full_Status(self):
#         return self.Status.Name
#
#     def get_full_UserType(self):
#         return self.UserType.Name
#
#     def get_full_AccessLevel(self):
#         return self.AccessLevel.Name
#
#     class Meta:
#         managed = False
#         db_table = 'UserManager'
#
# class TerritoryNew(models.Model):
#     TerritoryID = models.AutoField(primary_key=True, db_column='TerritoryID')
#     TerritoryCode = models.CharField(max_length=50, db_column='TerritoryCode')
#     TerritoryName = models.CharField(max_length=100, db_column='TerritoryName')
#     AreaName =  models.ForeignKey(AreaNew, db_column='AreaID', on_delete=models.CASCADE)
#     Notes = models.CharField(max_length=100, db_column='Notes')
#
#     def __str__(self):
#         return self.TerritoryName
#
#     class Meta:
#         managed = False
#         db_table = 'TerritoryNew'
#
# class Technician(models.Model):
#     Id = models.AutoField(primary_key=True, db_column='TechnicianID')
#     TechnicianName = models.CharField(max_length=50, db_column='TechnicianName')
#     Designation = models.CharField(max_length=100, db_column='Designation')
#     StaffID = models.CharField(max_length=100, db_column='StaffID')
#     MobileNo = models.CharField(max_length=100, db_column='MobileNo')
#     BloodGroup = models.CharField(max_length=100, db_column='BloodGroup')
#     TerritoryCode = models.CharField(max_length=100, db_column='TerritoryCode')
#     Notes = models.CharField(max_length=100, db_column='Notes')
#     EntryBy =  models.ForeignKey(UserManager, db_column='SupervisorCode', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.TechnicianName
#
#     class Meta:
#         managed = False
#         db_table = 'Technician'