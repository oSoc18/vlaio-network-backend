from .models import Company, Interaction, Partner, Overlap
import random as rnd
from datetime import date
from itertools import combinations
from django.db.models import Count
from datetime import datetime, timedelta


def calculateOverlap():
    overlaps = []

    partnerNames = []
    partners = Partner.objects.all()
    for p in partners:
        partnerNames.append(p.name)

    for partner in partners:
        # overlapSingle = Interaction.objects.raw(f"select interaction.company_id as id, count(company_id) as amount from main_interaction interaction JOIN main_partner partner on interaction.partner_id = partner.id WHERE partner.name = '{partner.name}' GROUP BY interaction.company_id")
        overlapSingle = Interaction.objects.filter(partner__name=partner.name).values(
            "company__vat").annotate(amount=Count("company__vat"))

        Interaction.objects.filter()
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
            query = ""
            for p in per:
                query += f"partner.name = '{p}' OR "
            query = query[:-3]

            #overlapedInteractions = Interaction.objects.raw("select interaction.company_id as id, count(company_id) as amount from main_interaction interaction JOIN main_partner partner on interaction.partner_id = partner.id WHERE "+query+"GROUP BY interaction.company_id")
            overlapedInteractions = Interaction.objects.filter(partner__name__in=per).values(
                "company__vat").annotate(amount=Count("company__vat"))

            amount = 0
            for interaction in overlapedInteractions:
                if(interaction["amount"] == 2):
                    amount += 1

            overlap = Overlap(partners=per, amount=amount)
            overlaps.append(overlap)

    return overlaps


def calculateOverlap_filterType(type):
    overlaps = []

    partnerNames = []
    partners = Partner.objects.all()
    for p in partners:
        partnerNames.append(p.name)

    for partner in partners:
        # overlapSingle = Interaction.objects.raw(f"select interaction.company_id as id, count(company_id) as amount from main_interaction interaction JOIN main_partner partner on interaction.partner_id = partner.id WHERE partner.name = '{partner.name}' GROUP BY interaction.company_id")
        overlapSingle = Interaction.objects.filter(partner__name=partner.name, type=type).values(
            "company__vat").annotate(amount=Count("company__vat"))

        Interaction.objects.filter()
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
            query = ""
            for p in per:
                query += f"partner.name = '{p}' OR "
            query = query[:-3]

            #overlapedInteractions = Interaction.objects.raw("select interaction.company_id as id, count(company_id) as amount from main_interaction interaction JOIN main_partner partner on interaction.partner_id = partner.id WHERE "+query+"GROUP BY interaction.company_id")
            overlapedInteractions = Interaction.objects.filter(partner__name__in=per, type=type).values(
                "company__vat").annotate(amount=Count("company__vat"))

            amount = 0
            for interaction in overlapedInteractions:
                if(interaction["amount"] == 2):
                    amount += 1

            overlap = Overlap(partners=per, amount=amount)
            overlaps.append(overlap)

    return overlaps


def calculateOverlap_timeframe(timeframe):
    overlaps = []

    interactions_between_timeframe = []

    for company in Company.objects.all():
        companyInteractions =company.interaction_set.all()
        for inter in companyInteractions:
            for inter2 in companyInteractions:
                if inter.id != inter2.id:
                    if calculateTimeDifference(inter.date, inter2.date) <= float(timeframe):
                        interactions_between_timeframe.append(inter.id)
            
    print("between timeframe: ",len(interactions_between_timeframe))
    print("All:",len(Interaction.objects.all()))

    partnerNames = []
    partners = Partner.objects.all()
    for p in partners:
        partnerNames.append(p.name)

    for partner in partners:
        # overlapSingle = Interaction.objects.raw(f"select interaction.company_id as id, count(company_id) as amount from main_interaction interaction JOIN main_partner partner on interaction.partner_id = partner.id WHERE partner.name = '{partner.name}' GROUP BY interaction.company_id")
        overlapSingle = Interaction.objects.filter(partner__name=partner.name, id__in = interactions_between_timeframe).values(
            "company__vat").annotate(amount=Count("company__vat"))

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
            query = ""
            for p in per:
                query += f"partner.name = '{p}' OR "
            query = query[:-3]

            #overlapedInteractions = Interaction.objects.raw("select interaction.company_id as id, count(company_id) as amount from main_interaction interaction JOIN main_partner partner on interaction.partner_id = partner.id WHERE "+query+"GROUP BY interaction.company_id")
            overlapedInteractions = Interaction.objects.filter(partner__name__in=per, id__in = interactions_between_timeframe).values(
                "company__vat").annotate(amount=Count("company__vat"))

            amount = 0
            for interaction in overlapedInteractions:
                if(interaction["amount"] == 2):
                    amount += 1

            overlap = Overlap(partners=per, amount=amount)
            overlaps.append(overlap)

    return overlaps


def calculateTimeDifference(date1,date2):
    return abs((date1 - date2).days / 7)
