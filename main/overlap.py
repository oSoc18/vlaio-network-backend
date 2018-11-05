from .models import Company, Interaction, Partner, Overlap
import random as rnd
from datetime import date
import time
from itertools import combinations
from django.db.models import Count
from datetime import datetime, timedelta

"""
limit = int
types = string in vorm van: a,b,c of a 
timeframe = int
timeinterval = [int begin, int eind]

1. check which filters are passed (if not none)
2. the overlap is calculated using a list of partners names, fill this list
3. calculate single overlaps 
    why single overlaps? -> combinations instead of permutations to avoid: [een,twee] & [twee,een]
    also, single overlaps need to be calculated using a different sql query
4. calculate main overlaps.
    - generate combinations
    - for each combination, run sql query
    - for each result of the sql query, loop through and select the overlap

SQL query changes based on filters that are provided. -> if statements
"""
def caclOverlap(limit, types, timeframe, timeInterval):
    overlaps = []
    partnerNames = []
    interaction_types = []
    interactions_between_timeframe = [] 

    filterTypes = False
    filterTimeframe = False

    #1. filter checks
    if types is not None:
        #types = subsidie,advies,... => ["subsidie","advies","..."]
        interaction_types = types.split(',')
        
        filterTypes = True

    if timeframe is not None:
        filterTimeframe = True
        
        for company in Company.objects.all():
            companyInteractions =company.interaction_set.all()
            for inter in companyInteractions:
                for inter2 in companyInteractions:
                    if inter.id != inter2.id:
                        if calculateTimeDifference(inter.date, inter2.date) <= float(timeframe):
                            interactions_between_timeframe.append(inter.id)

    if limit is not None:
        #find interesting parners to calculate overlap from based on interaction amount
        interestingPartners = Interaction.objects.values("partner__id").annotate(amount=Count("partner__id")).order_by('-amount')
        idList = []
        for i,partner in enumerate(interestingPartners):
            if i+1 <= int(limit):
                idList.append(partner["partner__id"])
        partners = Partner.objects.filter(id__in=idList)
    else:
        partners = Partner.objects.all()

    #2. fill list of partner names
    for p in partners:
        partnerNames.append(p.name)


    

    #3. single overlaps
    for partner in partners:
        #define filter arguments

        kwargs = {
            "partner__name": partner.name,
            "id__in": interactions_between_timeframe,
            "type__in": interaction_types
        }

        if not filterTimeframe:
            del kwargs["id__in"]
        if not filterTypes:
            del kwargs["type__in"]

        overlapSingle = Interaction.objects.filter(**kwargs).values("company__vat").annotate(amount=Count("company__vat"))
    

        amount = 0
        for singleI in overlapSingle:
            amount += 1

        par = []
        par.append(partner.name)

        overlap = Overlap(partners=par, amount=amount)
        overlaps.append(overlap)
    
    
    for i, partner in enumerate(partnerNames):
        
        perm = combinations(partnerNames, i+2)
        
        for per in perm:
            
            kwargs = {
                "partner__name__in": per,
                "id__in": interactions_between_timeframe,
                "type__in": interaction_types
            }

            if not filterTimeframe:
                del kwargs["id__in"]
            if not filterTypes:
                del kwargs["type__in"]

            print(kwargs)

            overlapedInteractions = Interaction.objects.filter(**kwargs).values("company__vat").annotate(amount=Count("company__vat"))


            amount = 0
            for interaction in overlapedInteractions:
                if(interaction["amount"] == len(per)):
                    amount += 1

            overlap = Overlap(partners=per, amount=amount)
            overlaps.append(overlap)
        
    return overlaps

def calculateTimeDifference(date1,date2):
    return abs((date1 - date2).days / 7)
