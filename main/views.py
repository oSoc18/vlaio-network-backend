from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Company, Interaction, Partner, Overlap, DataFile
from .serializers import CompanySerializer, InteractionSerializer, PartnerSerializer, OverlapSerializer, DataFileSerializer
from excel_parse import COMPANY_CONFIG, INTERACTION_CONFIG
from django.conf import settings
from .overlap import calculateOverlap, calculateOverlap_filterType

"""
class Home(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.all()
        return context
"""


class CompanyListView(ListAPIView):
    serializer_class = CompanySerializer
    queryset = Company.objects.all()


class InteractionListView(ListAPIView):
    serializer_class = InteractionSerializer

    def get_queryset(self):
        interactions = Interaction.objects.all()
        partner_name = self.request.query_params.get('name', None)

        if partner_name is not None:
            partner = Partner.objects.get(name=partner_name)
            interactions = interactions.filter(partner_id=partner.id)
            # interactions = interactions.filter(partner__name=partner_name.upper())
        return interactions


class PartnerListView(ListAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()


class OverlapListView(ListAPIView):
    serializer_class = OverlapSerializer

    def get_queryset(self):
        return calculateOverlap()


class OverlapTimeframeListView(ListAPIView):
    serializer_class = OverlapSerializer

    def get_queryset(self):
        interaction_type = self.request.query_params.get('type', None)
        if interaction_type is not None:
            return calculateOverlap_filterType(interaction_type)
        


class DataFileView(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):

        file_serializer = DataFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            # COMPANY_CONFIG.insert_from_excel(settings.MEDIA_ROOT+"/belfirst1.xlsx")
            INTERACTION_CONFIG.insert_from_excel(
                settings.MEDIA_ROOT+"/VLAIO_advice.xlsx")
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
