from rest_framework.serializers import ModelSerializer, CharField

from .models import Company, Interaction,Partner,Overlap, DataFile


class InteractionOfCompaySerializer(ModelSerializer):
    partner = CharField(source='partner.name')

    class Meta:
        model = Interaction
        fields = (
            'id',
            'partner',
            'date',
            'type'
        )

class CompanySerializerInteractions(ModelSerializer):
    interaction_set = InteractionOfCompaySerializer(many=True)

    class Meta:
        model = Company
        fields = (
            'vat',
            'name',
            'interaction_set',
            'employees',
            'profit',
        )


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = (
            'vat',
            'name',
            'employees',
            'profit',
        )

class InteractionSerializer(ModelSerializer):

    class Meta:
        model = Interaction
        fields = (
            'id',
            'type',
            'date',
            'company_id',
            'partner_id'
        )

class OverlapSerializer(ModelSerializer):
    class Meta:
        model = Overlap
        fields = (
            'partners',
            'amount'
        )

class PartnerSerializer(ModelSerializer):

    class Meta:
        model = Partner
        fields = (
            'id',
            'name'
        )


class DataFileSerializer(ModelSerializer):
  class Meta():
    model = DataFile
    fields = ('file', 'timestamp','userid')
