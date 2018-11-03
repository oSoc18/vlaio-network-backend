"""
A checker is a function that take a dataframe returns
a tuple of (str, bool) (text, is_warining)
if is_warning is False means that it is an error
"""
import pandas as pd
from main.models import Company, Interaction, Partner
from .vat_normilze import is_vat

def check_new_parnter(df):
    partners_xl = df["Source"].unique()
    partners_db = Partner.objects.values_list('name', flat=True).filter(name__in=partners_xl).distinct()
    partners_new = set(partners_xl) - set(partners_db)
    if len(partners_new):
        return f"{len(partners_new)} partners will be added" + " ".join(partners_new)


def check_new_types(df):
    types_xl = df["Type"].unique()
    types_db = Interaction.objects.values_list('type', flat=True).exclude(type__in=types_xl).distinct()
    types_new = set(types_xl) - set(types_db)
    if len(types_new):
        return f"{len(types_new)} types will be added to the database " + " ".join(types_new), True


def check_empty_col(col_name):
    def checker(df):
        res = df.index[(df[col_name] == "") | (df[col_name] == "nan")] + 1
        if len(res):
            return f"{len(res)} rows contains empty {col_name}: {list(res[:3])}", False
    return checker


def check_new_vat(df):
    vat_excl = set(df["VAT"].unique())
    vat_db = set(Company.objects.filter(vat__in=vat_excl).values_list('vat', flat=True))
    vat_news = vat_excl - vat_db

    if vat_news:
        return f"{len(vat_news)} vat are not in the database and will be added " + " ".join(vat_news), True

"""
def check_empty_type(df):
    res = df.index[df["Type"] == ""] + 1
    if len(res):
        return f"{len(res)} rows contains empty types: {list(res[:3])}", False
"""

def check_tva(df):
    res = df.index[df["VAT"].apply(lambda x: not is_vat(x))] + 1
    if len(res):
        return f"{len(res)} rows contains bad VAT among which: {list(res[:3])}", False
