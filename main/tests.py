from django.test import TestCase

# Create your tests here.


"""
parnters = Partner.objects.all()
dicts = {
  "name": "Partners",
  "children": []
}

depth = 4
def add_layer(dict, d):
    if d == 0:
        return
    for p in parnters:
        new_dict = {'name': p.name, 'children': [], 'size': 0}
        dict["children"].append(new_dict)
        add_layer(new_dict, d - 1)
add_layer(dicts, 4)
print(dicts)

companies = Company.objects.all()
for comp in companies:
    interactions = Interaction.objects.filter(company_id=comp.id).order_by('date')
    current = dicts
    for i in interactions:
        dicts i.partner_id == i.partner_id
"""