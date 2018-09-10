import random as rnd
from datetime import date

import django
# before importing any model
django.setup()

from main.models import Company, Partner, Interaction

COMPANIES_COUNT = 1000

print("Begin mock insertion")


PARTNERS = {
    # NAME: MAX_INTERACTIONS
    '00 APPLE': 750,
    '00 BANANA': 600,
    '00 MANGO': 500,
    '00 CAROT': 400,
    "00 ORANGE": 300,
    "00 CHERRY": 200
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

Partner.objects.bulk_create([
    Partner(id=name, name=name)
    for name in PARTNERS
])

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
            partner_id=part
        ) for i, vat in enumerate(interactions)
    ])

print("Finished insertion")
