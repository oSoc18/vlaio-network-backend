from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Company, Interaction, Partner, Overlap, DataFile
from .serializers import CompanySerializer, InteractionSerializer, PartnerSerializer, OverlapSerializer, DataFileSerializer
from excel_parse import COMPANY_CONFIG, INTERACTION_CONFIG
from django.conf import settings
from .overlap import calculateOverlap, calculateOverlap_filterType,calculateOverlap_timeframe

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

###############################################################################

@api_view()
def view(request):
    companies = Company.objects.all()
    partners = Partner.objects.all()
    partners_by_name = {
        p.name: p for p in partners
    }
    partners_by_id = {
        p.id: p for p in partners
    }

    dicts = {
        "name": "Partners",
        "children": []
    }
    for n in companies:
        current = dicts
        interactions = Interaction.objects.filter(company_id=n.vat).order_by('date')
        for i, m in enumerate(interactions):
            found_dict = None
            for _d in current["children"]:
                name = _d["name"]
                if m.partner_id == partners_by_name[name].id:
                    found_dict = _d
                    break
            if not found_dict:
                found_dict = {
                    "name": partners_by_id[m.partner_id].name,
                    "children": []
                }
            current["children"].append(found_dict)
            if i == len(interactions) - 1:
                # last
                current.setdefault("size", 0)
                current["size"] += 1
            else:
                current = found_dict

    return Response(dicts)
###############################################################################



class OverlapListView(ListAPIView):
    serializer_class = OverlapSerializer 

    def get_queryset(self):
        return calculateOverlap()


class OverlapTimeframeListView(ListAPIView):
    serializer_class = OverlapSerializer

    def get_queryset(self):
        interaction_type = self.request.query_params.get('type', None)
        timeframe = self.request.query_params.get('timeframe', None)

        if interaction_type is not None:
            return calculateOverlap_filterType(interaction_type)
        elif timeframe is not None:
            return calculateOverlap_timeframe(timeframe)
        


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

class InteractionTypeListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(Interaction.objects.values_list('type', flat=True).distinct())
