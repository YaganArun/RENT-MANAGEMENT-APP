from django.db import models
class Person(models.Model):
    first_name = models.CharField(max_length=30,null=False,blank=False)
    last_name = models.CharField(max_length=30,null=True,blank=True)
    age = models.IntegerField(null=True)
    designation = models.CharField(max_length=30,null=True,blank=True)
    room_no = models.CharField(max_length=30)
    id = models.CharField(primary_key=True,unique=True,max_length=20)
    rent_Ammount = models.IntegerField()
    advance_Ammount = models.IntegerField()
    contact_no = models.IntegerField(null=True)
    date = models.DateField()

class Rent(models.Model):
    #id = models.IntegerField(primary_key=True)
    person = models.ForeignKey(Person , on_delete=models.CASCADE)
    rent = models.IntegerField()
    electric_bill = models.IntegerField()
    Maintanace_charge = models.IntegerField(null=True,blank=True)
    paymentDate = models.DateField(unique=False)

class PersonTrack(models.Model): #itilize for a new db with length
    id = models.IntegerField(primary_key=True)
    length = models.IntegerField()

class Record(models.Model):  #intilize for a new db with actionMonth
    actionMonth = models.IntegerField(primary_key=True,unique=True)
    count = models.IntegerField( default=0)
    #for i in range(1,13):
        #Record.objects.create(actionMonth = i)







