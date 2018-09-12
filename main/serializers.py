from rest_framework.serializers import ModelSerializer

from .models import Company, Interaction,Partner,Overlap


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
