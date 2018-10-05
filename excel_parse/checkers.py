"""
A checker is a function that take a dataframe returns
a tuple of (str, bool) (text, is_warining)
if is_warning is False means that it is an error
"""
import pandas as pd
from main.models import Company, Interaction, Partner
from .vat_normilze import is_vat

def check_new_parnter(df):
    partners = Partner.objects.exclude(name__in=df["Source"].unique())
    if len(partners):
        return f"{len(partners)} partners will be added" + " ".join(map(lambda p: p.name, partners))


def check_new_types(df):
    types_excl = df["Type"].unique()
    types_db = Interaction.objects.exclude(type__in=types_excl).values_list('type', flat=True).distinct()
    if len(types_db):
        return f"{len(types_db)} types will be added to the database " + " ".join(types_db), True


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
    print(df)
    if len(res):
        return f"{len(res)} rows contains bad VAT: {list(res[:3])}", False
