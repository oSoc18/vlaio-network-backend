"""
This example will insert all companies from an excel file
"""
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'vlaio_prototype.settings'
import django

# before importing any model
django.setup()

from . import INTERACTION_CONFIG

file_path = "D:\\Downloads\\wetransfer-470901\\VLAIO advice.xlsx"

INTERACTION_CONFIG.insert_from_excel(file_path)
