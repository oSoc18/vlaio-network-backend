from datetime import date
import pandas as pd
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'vlaio_prototype.settings'
import django
# before importing any model
django.setup()

from main.models import Company, Interaction, Partner

from .vat_normilze import normalize, is_vat
from . import checkers


class Config:
    def __init__(self, xl_to_sql, model_class, xl_types=None, map_df_func=None, checkers=None, map_df_read=None):
        self.xl_to_sql = xl_to_sql
        self.xl_types = xl_types
        self.xl_cols = set(xl_to_sql.keys())
        self.model_class = model_class
        self.map_df_func=map_df_func
        self.map_df_read=map_df_read
        self.checkers = checkers or []

    def insert_models(self, df):
        if self.map_df_func is not None:
            df = self.map_df_func(df)
        dicts = df.to_dict('records')
        self.model_class.objects.bulk_create(
            [
                self.model_class(**{self.xl_to_sql[k]: d[k] for k in self.xl_cols})
                for d in dicts
            ]
        )
    
    def check(self, df):
        """
        return a tuple of (errors, warnings)
        """
        res = filter(lambda x: x, [f(df) for f in self.checkers])
        warnings = []
        errors = []
        res = list(res)
        for txt, is_warning in res:
            if is_warning:
                warnings.append(txt)
            else:
                errors.append(txt)
        return errors, warnings

    def insert_from_excel(self, file_path):
        df = self.get_data_from_excel_file(file_path)
        self.insert_models(df)

    def get_data_from_excel_file(self, file_path):
        df = pd.read_excel(
            file_path,
            encoding='sys.getfilesystemencoding()',
            dtype=self.xl_types
        )
        if self.map_df_read is not None:
            df = self.map_df_read(df)
        present = set(df.columns)
        missing = self.xl_cols - present
        if missing:
            raise ValueError("Missing columns: " + ",".join(missing))
        additional = present - self.xl_cols
        for col in additional:
            del df[col]

        return df




def map_company_vat(df):
    df["VAT"] = df["VAT"].apply(normalize)
    return df


COMPANY_CONFIG = Config(
    xl_to_sql={
        # In file name: db column name
        "Naam": "name",
        "VAT": "vat",
        "werknemers": "employees",
        "winst": "profit"
    },
    xl_types={
        "Naam": str,
        "VAT": str,
        "werknemers": int,
        "winst": int
    },
    model_class=Company,
    map_df_func=map_company_vat,
    checkers=[checkers.check_tva, checkers.check_empty_col("Naam")]
)


def map_df_interactions(df: pd.DataFrame):
    sources = {
        name: Partner.objects.get_or_create(name=name)[0]
        for name in set(df['Source'])
    }
    df["Source"] = df["Source"].apply(lambda x: sources[x].id)
    df["VAT"] = df["VAT"].apply(normalize)
    return df


def map_df_interactions_read(df):
    df["VAT"] = df["VAT"].apply(normalize)
    return df


INTERACTION_CONFIG = Config(
    xl_to_sql={
        "VAT": "company_id",
        "Source": 'partner_id',
        "Type": "type",
        "Date": "date"
    },
    xl_types={
        "Source": str,
        "Type": str,
        "VAT": str,
        "date": date
    },
    model_class=Interaction,
    map_df_func=map_df_interactions,
    checkers=[
        checkers.check_new_parnter,
        checkers.check_new_types,
        checkers.check_empty_col("Source"),
        checkers.check_empty_col("Date"),
        checkers.check_empty_col("Type"),
        checkers.check_new_vat,
        checkers.check_tva
    ],
    map_df_read=map_df_interactions_read
)
