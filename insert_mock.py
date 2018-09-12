import random as rnd
from datetime import date
from itertools import combinations

import django
# before importing any model
django.setup()

from main.models import Company, Partner, Interaction, Overlap

COMPANIES_COUNT = 1000

print("Begin mock insertion")


PARTNERS = {
    # NAME: MAX_INTERACTIONS
    'VLAIO': 750,
    'KULeuven': 600,
    'Unizo': 500,
    'NSZ': 400,
    "Voka": 300,
    "VUB": 200
}
MAX_COUNT = max(PARTNERS.values())

GENERATED_VATS = []


def random_vat():
    digits = list(map(str, range(10)))
    res = 'BE0' + "".join(rnd.choice(digits) for i in range(9))
    GENERATED_VATS.append(res)
    return res


def random_company_name():
    alphabet = list(map(chr, range(ord('A'), ord('Z') + 1)))
    return "".join(rnd.choice(alphabet) for i in range(rnd.randint(4, 10)))


Company.objects.bulk_create([
    Company(
        vat=random_vat(),
        name=random_company_name(),
        employees=rnd.randint(-1, 1000),
        profit=rnd.randint(-1_000_000, 1_000_000_000)
    ) for i in range(COMPANIES_COUNT)
])

partners = [
    Partner(name=name)
    for name in PARTNERS
]

for partner in partners : 
    partner.save()

for index, (part, count) in enumerate(PARTNERS.items()):
    interactions = {
        rnd.choice(GENERATED_VATS)
        for i in range(count)
    }
    Interaction.objects.bulk_create([
        Interaction(
            id=str(index*MAX_COUNT+i)+vat,
            type='ad',
            date=date.today(),
            company_id=vat,
            partner_id=partners[index].id
        ) for i, vat in enumerate(interactions)
    ])


partnerNames = []
for partner in partners:
    partnerNames.append(partner.name)


for partner in partners:
    overlapSingle = Interaction.objects.raw(f"select interaction.company_id as id, count(company_id) as amount from main_interaction interaction JOIN main_partner partner on interaction.partner_id = partner.id WHERE partner.name = '{partner.name}' GROUP BY interaction.company_id")
    amount = 0
    for singleI in overlapSingle:
        amount+= 1  

    par = []
    par.append(partner)
    
    overlap = Overlap(partners=par, amount=amount)
    overlap.save()

for i, partner in enumerate(partnerNames):


    perm = combinations(partnerNames,i+2)
    for per in perm:
        query=""
        for p in per:
            query+= f"partner.name = '{p}' OR "
        query = query[:-3]

        overlapedInteractions = Interaction.objects.raw("select interaction.company_id as id, count(company_id) as amount from main_interaction interaction JOIN main_partner partner on interaction.partner_id = partner.id WHERE "+query+"GROUP BY interaction.company_id")
        amount = 0
        for interaction in overlapedInteractions: 
            if(interaction.amount == 2):
                amount+= 1
    


        overlap = Overlap(partners=per, amount=amount)
        overlap.save()

print("Finished insertion")
