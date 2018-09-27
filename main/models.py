from django.contrib.postgres.fields import ArrayField
from django.db import models

class Company(models.Model):
    vat = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=120)
    employees = models.IntegerField()
    profit = models.BigIntegerField(null=True)


class Partner(models.Model):
    #id = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=400)
    children = ArrayField(models.CharField(max_length=400))

class Overlap(models.Model):
    #partners = models.CharField(max_length=400)
    partners = ArrayField(models.CharField(max_length=400))
    amount = models.IntegerField()

class Interaction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    type = models.CharField(max_length=200)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)

class DataFile(models.Model):
  file = models.FileField(blank=False, null=False)
  timestamp = models.DateTimeField(auto_now_add=True)