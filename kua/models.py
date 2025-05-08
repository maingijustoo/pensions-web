from django.db import models


class Employers(models.Model):
    employerid = models.AutoField(db_column='EmployerID', primary_key=True)
    employername = models.CharField(max_length=100)
    employerkrapin = models.CharField(max_length=50, unique=True)
    contactperson = models.CharField(max_length=100, blank=True, null=True)
    contactemail = models.CharField(max_length=100, unique=True, blank=True, null=True)
    contactphone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Employers'


class Members(models.Model):
    memberid = models.AutoField(db_column='MemberID', primary_key=True)
    fullname = models.CharField(max_length=100)
    dateofbirth = models.DateField()
    contactnumber = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    nssfcardnumber = models.CharField(max_length=50, unique=True, blank=True, null=True)
    krapin = models.CharField(max_length=50, unique=True, blank=True, null=True)
    registrationdate = models.DateTimeField(blank=True, null=True)
    employmentstatus = models.CharField(max_length=20, blank=True, null=True)
    employerid = models.ForeignKey(Employers, models.DO_NOTHING, db_column='EmployerID', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Members'


class Contributions(models.Model):
    contributionid = models.AutoField(db_column='ContributionID', primary_key=True)
    memberid = models.ForeignKey(Members, models.DO_NOTHING, db_column='MemberID')
    employerid = models.ForeignKey(Employers, models.DO_NOTHING, db_column='EmployerID', blank=True, null=True)
    contributiondate = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paymentmethod = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'Contributions'


class Dependents(models.Model):
    dependentid = models.AutoField(db_column='DependentID', primary_key=True)
    memberid = models.ForeignKey(Members, models.DO_NOTHING, db_column='MemberID')
    dependentname = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50, blank=True, null=True)
    dateofbirth = models.DateField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Dependents'


class MembersBackup(models.Model):
    memberid = models.AutoField(db_column='MemberID', primary_key=True)
    fullname = models.CharField(max_length=100)
    dateofbirth = models.DateField()
    contactnumber = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    nssfcardnumber = models.CharField(max_length=50, blank=True, null=True)
    krapin = models.CharField(max_length=50, blank=True, null=True)
    registrationdate = models.DateTimeField(blank=True, null=True)
    employmentstatus = models.CharField(max_length=20, blank=True, null=True)
    employerid = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Members_Backup'


class Payments(models.Model):
    paymentid = models.AutoField(db_column='PaymentID', primary_key=True)
    memberid = models.ForeignKey(Members, models.DO_NOTHING, db_column='MemberID')
    paymentdate = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    paymenttype = models.CharField(max_length=50)
    processedby = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Payments'
