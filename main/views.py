import os.path
from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Company, Interaction, Partner, Overlap, DataFile
from .serializers import CompanySerializer, InteractionSerializer, PartnerSerializer, OverlapSerializer, DataFileSerializer
from excel_parse import COMPANY_CONFIG, INTERACTION_CONFIG
from excel_parse.checkers import get_new_vat
from django.conf import settings
from .overlap import caclOverlap

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
    """
    params: max_depth(int)
    criteria: two possibles values are "partner" (default) and "interaction"
    """
    MAX_DEPTH = int(request.query_params.get('max_depth', 4))
    PATH_INTERACTION_TYPE = (
        request.query_params.get('criteria', 'partner')
        == 'interaction'
    )

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
        current = dicts

    return Response(dicts)


"""
@api_view()
def view(request):
    # Parameters and filters: TODO: make this come from url params
    MAX_DEPTH = 400

    # True if it is by interaction type
    # False if it is by partner
    PATH_INTERACTION_TYPE = partner

    companies = Company.objects.all()

    if PATH_INTERACTION_TYPE == partner:
        partners = Partner.objects.all()
        partners_by_name = {
            p.name: p for p in partners
        }
        partners_by_id = {
            p.id: p for p in partners
        }
    elif PATH_INTERACTION_TYPE == company:
        companies_by_name = {
            p.name: p for p in companies
        }
        companies_by_id = {
            p.vat: p for p in companies
        }
    else:
        inter = Interaction.objects.all()
        interactions_by_id = {
            p.id: p for p in inter
        }
    def get_name(record):
        if PATH_INTERACTION_TYPE == company:
            return companies_by_id[record.companies_id].name
        elif PATH_INTERACTION_TYPE == partner:
            return partners_by_id[record.partner_id].name
        else:
            return interactions_by_id[record.interactions_id].type

    def is_corresponding(record, name):
        if PATH_INTERACTION_TYPE == company:
            return record.companies_id == companies_by_name[name].vat
        elif PATH_INTERACTION_TYPE == partner:
            return record.partner_id == partners_by_name[name].id
        else:
            return record.interactions_id == interations_by_type[type].id

    dicts = {
        "name": "Partners" if PATH_INTERACTION_TYPE==partner elif PATH_INTERACTION_TYPE==company "Companies" else  "Interactions types",
        "children": []
    }
    **********************************************************************************************************************
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

"""


class OverlapListView(ListAPIView):
    serializer_class = OverlapSerializer 
    
    def get_queryset(self):
        limit = self.request.query_params.get('limit', None)
        interaction_types = self.request.query_params.get('type', None)
        timeframe = self.request.query_params.get('timeframe', None)
        
        interval_begin = self.request.query_params.get('begin', None)
        interval_end = self.request.query_params.get('end', None)
        
        return caclOverlap(limit, interaction_types, timeframe, interval_begin, interval_end)



class DataFileView(APIView):
    """
    Upload excel file

    POST:
    if there is errors the file is not conserved and the returned object is
    {errors: string[], warnings: string[]}
    
    if it contains only warning or no warning it is not deleted
    and it return  an object:  {id: int, warnings: string[]}
    """
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        
        file_serializer = DataFileSerializer(data=request.data)
        if file_serializer.is_valid():
            filedata = file_serializer.save()
            # COMPANY_CONFIG.insert_from_excel(settings.MEDIA_ROOT+"/belfirst1.xlsx")
            data = INTERACTION_CONFIG.get_data_from_excel_file(
                os.path.join(settings.MEDIA_ROOT, filedata.file.name)
            )
            errors, warnings = INTERACTION_CONFIG.check(data)
            resp_data = {'warnings': warnings}
            if errors:
                filedata.delete()
                os.remove(os.path.join(settings.MEDIA_ROOT, filedata.file.name))
                resp_data['errors'] = errors
            else:
                resp_data['upload_id'] = filedata.id

            return Response(resp_data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def apply_datafile(request, id):
    """
    url_params: id(int) id returned by the upload/ endpoint

    code: 204 on succes, 404 if id does not exist, 401 if already applied
    """
    filedata = get_object_or_404(DataFile, pk=id)
    if filedata.applied:
        return Response({'error': 'already applied'}, status=401)

    data = INTERACTION_CONFIG.get_data_from_excel_file(
        os.path.join(settings.MEDIA_ROOT, filedata.file.name)
    )
    vat_list = get_new_vat(data)
    if vat_list:
        Company.objects.bulk_create(map(lambda x: Company(vat=x, employees=0), vat_list))
    INTERACTION_CONFIG.insert_models(data)
    filedata.applied = True
    filedata.save()
    return Response(status=204)


class InteractionTypeListView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(Interaction.objects.values_list('type', flat=True).distinct())
