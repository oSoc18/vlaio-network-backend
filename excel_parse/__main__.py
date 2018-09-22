"""
This example will insert all companies from an excel file
"""
import os
from operator import itemgetter
os.environ['DJANGO_SETTINGS_MODULE'] = 'vlaio_prototype.settings'
import django

# before importing any model
django.setup()

from . import INTERACTION_CONFIG

file_path = "/home/ahmed/Documents/VLAIO/Parts/Partner1.xlsx"
data = INTERACTION_CONFIG.get_data_from_excel_file(file_path)
errors = INTERACTION_CONFIG.check(data)
if all(map(lambda err: err is None or err[0], errors)):
    print(*(map(lambda x: "" if x is None else errors[0], errors)), sep="\n")
    print("Will insert but warinings!")
    INTERACTION_CONFIG.insert_models(data)
else:
    print("Will not insert because errors")
