from django.db import models

# Create your models here.

class Status(models.Model):
    Id = models.AutoField(primary_key=True, db_column='Id')
    Name = models.CharField(max_length=50, db_column='Name')

    def __str__(self):
        return self.Name

    class Meta:
        managed = False
        db_table = 'Status'

class AreaNew(models.Model):
    Id = models.AutoField(primary_key=True, db_column='AreaID')
    Name = models.CharField(max_length=100, db_column='AreaName')

    def __str__(self):
        return self.Name

    class Meta:
        managed = False
        db_table = 'AreaNew'

class UserManager(models.Model):
    UserID = models.AutoField(primary_key=True, db_column='UserID')
    UserName = models.CharField(max_length=255, db_column='UserName', unique=True)
    Password = models.CharField(max_length=255, db_column='Password')        
    Status =  models.ForeignKey(Status, db_column='Status', on_delete=models.CASCADE)
    AccessLevel = models.ForeignKey(AreaNew, db_column='AccessLevel', on_delete=models.CASCADE)
    DisplayName = models.CharField(max_length=100, db_column='DisplayName')

    def __str__(self):
       return "Username: " + self.UserName + " has been created successfully."

    def get_full_name(self):
        return self.UserName

    def get_full_Status(self):
        return self.Status.Name

    def get_full_UserType(self):
        return self.UserType.Name

    def get_full_AccessLevel(self):
        return self.AccessLevel.Name

    class Meta:
        managed = False
        db_table = 'UserManager'

class TerritoryNew(models.Model):
    TerritoryID = models.AutoField(primary_key=True, db_column='TerritoryID')
    TerritoryCode = models.CharField(max_length=50, db_column='TerritoryCode')
    TerritoryName = models.CharField(max_length=100, db_column='TerritoryName')
    AreaName =  models.ForeignKey(AreaNew, db_column='AreaID', on_delete=models.CASCADE)
    Notes = models.CharField(max_length=100, db_column='Notes')

    def __str__(self):
        return self.TerritoryName

    class Meta:
        managed = False
        db_table = 'TerritoryNew'

class Technician(models.Model):
    Id = models.AutoField(primary_key=True, db_column='TechnicianID')
    TechnicianName = models.CharField(max_length=50, db_column='TechnicianName')
    Designation = models.CharField(max_length=100, db_column='Designation')
    StaffID = models.CharField(max_length=100, db_column='StaffID')
    MobileNo = models.CharField(max_length=100, db_column='MobileNo')
    BloodGroup = models.CharField(max_length=100, db_column='BloodGroup')
    TerritoryCode = models.CharField(max_length=100, db_column='TerritoryCode')
    Notes = models.CharField(max_length=100, db_column='Notes')
    EntryBy =  models.ForeignKey(UserManager, db_column='SupervisorCode', on_delete=models.CASCADE)

    def __str__(self):
        return self.TechnicianName

    class Meta:
        managed = False
        db_table = 'Technician'