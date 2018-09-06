from django.db import models


class Company(models.Model):
    vat = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=120)
    employees = models.IntegerField()
    profit = models.IntegerField(null=True)


class Partner(models.Model):
    id = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=30)


class Interaction(models.Model):
    ADVICE = 'ad'
    FINANCIAL_AID = 'fa'

    INTERACTION_TYPE = (
        (ADVICE, 'advice'),
        (FINANCIAL_AID, 'financial aid')
    )

    id = models.CharField(primary_key=True, max_length=30)
    date = models.DateField()
    type = models.CharField(max_length=2, choices=INTERACTION_TYPE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    partner = models.ForeignKey(Partner, on_delete=models.CASCADE)
