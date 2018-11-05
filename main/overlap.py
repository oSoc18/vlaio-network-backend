from .models import Company, Interaction, Partner, Overlap
import random as rnd
from datetime import date
import time
from itertools import combinations
from django.db.models import Count
from datetime import datetime, timedelta


def caclOverlap(limit, types, timeframe):
    overlaps = []
    partnerNames = []
    interactions_between_timeframe = [] 

    filterTypes = False
    filterTimeframe = False

    if types is not None:
        #types = subsidie,advies,... => ["subsidie","advies","..."]
        interaction_types_splitted = types.split(',')
        interaction_types = [','.join(interaction_types_splitted[n:]) for n in range(len(interaction_types_splitted))]
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
        print("between timeframe: ",len(interactions_between_timeframe))
        print("All:",len(Interaction.objects.all()))

    if limit is not None:
        partners = Partner.objects.all()[:int(limit):1]
    else:
        partners = Partner.objects.all()

    
    for p in partners:
        partnerNames.append(p.name)

   
    for partner in partners:
        
        print(filterTimeframe)
        
        if filterTypes:
            if filterTimeframe :
                overlapSingle = Interaction.objects.filter(partner__name=partner.name,id__in=interactions_between_timeframe,type__in=interaction_types).values(
                "company__vat").annotate(amount=Count("company__vat"))
            else:
                overlapSingle = Interaction.objects.filter(partner__name=partner.name,type__in=interaction_types).values(
                "company__vat").annotate(amount=Count("company__vat"))
        elif filterTimeframe:
            overlapSingle = Interaction.objects.filter(partner__name=partner.name,id__in=interactions_between_timeframe).values(
            "company__vat").annotate(amount=Count("company__vat"))
        else:
            overlapSingle = Interaction.objects.filter(partner__name=partner.name).values(
            "company__vat").annotate(amount=Count("company__vat"))

        amount = 0
        for singleI in overlapSingle:
            amount += 1

        par = []
        par.append(partner.name)

        overlap = Overlap(partners=par, amount=amount)
        overlaps.append(overlap)
    am = 0
    
    for i, partner in enumerate(partnerNames):
        
        perm = combinations(partnerNames, i+2)
        
        for per in perm:
            am = am + 1
            print(per)
            if filterTypes:
                if filterTimeframe :
                    overlapedInteractions = Interaction.objects.filter(partner__name__in=per, type__in=interaction_types,id__in=interactions_between_timeframe).values(
                    "company__vat").annotate(amount=Count("company__vat"))
                else:
                    overlapedInteractions = Interaction.objects.filter(partner__name__in=per, type__in=interaction_types).values(
                    "company__vat").annotate(amount=Count("company__vat"))
            elif filterTimeframe:
                overlapedInteractions = Interaction.objects.filter(partner__name__in=per, id__in=interactions_between_timeframe).values(
                "company__vat").annotate(amount=Count("company__vat"))
            elif filterTimeframe and filterTypes:
                overlapedInteractions = Interaction.objects.filter(partner__name__in=per, type__in=interaction_types,id__in=interactions_between_timeframe).values(
                "company__vat").annotate(amount=Count("company__vat"))
            else:
                start_time = time.time()
                overlapedInteractions = Interaction.objects.filter(partner__name__in=per).values(
                "company__vat").annotate(amount=Count("company__vat"))
                print("--- %s seconds ---" % (time.time() - start_time))


            
                
            amount = 0
            for interaction in overlapedInteractions:
                if(interaction["amount"] == len(per)):
                    amount += 1

            overlap = Overlap(partners=per, amount=amount)
            overlaps.append(overlap)
            print(am)
        
    return overlaps

def calculateTimeDifference(date1,date2):
    return abs((date1 - date2).days / 7)
