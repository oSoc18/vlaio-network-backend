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
    # Parameters and filters: TODO: make this come from url params
    MAX_DEPTH = 400
    
    # True if it is by interaction type
    # False if it is by partner
    PATH_INTERACTION_TYPE = False

    companies = Company.objects.all()

    if not PATH_INTERACTION_TYPE:
        partners = Partner.objects.all()
        partners_by_name = {
            p.name: p for p in partners
        }
        partners_by_id = {
            p.id: p for p in partners
        }

    def get_name(record):
        if PATH_INTERACTION_TYPE:
            return record.type
        else:
            return partners_by_id[record.partner_id].name
    
    def is_corresponding(record, name):
        if PATH_INTERACTION_TYPE:
            return record.type == name
        else:
            return record.partner_id == partners_by_name[name].id


    dicts = {
        "name": "Interactions types" if PATH_INTERACTION_TYPE else "Partners",
        "children": []
    }
    for n in companies:
        current = dicts
        interactions = Interaction.objects.filter(company_id=n.vat).order_by('date')[:MAX_DEPTH]
        for i, m in enumerate(interactions):
            found_dict = None
            for _d in current["children"]:
                name = _d["name"]
                if is_corresponding(m, name):
                    found_dict = _d
                    break
            if not found_dict:
                found_dict = {
                    "name": get_name(m),
                    "children": [],
                    "size": 0
                }
                current["children"].append(found_dict)
            found_dict["size"] += 1
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
