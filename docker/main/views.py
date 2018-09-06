from django.shortcuts import render
from .models import Company, Interaction,Partner
from .serializers import CompanySerializer, InteractionSerializer, PartnerSerializer
from rest_framework.generics import ListAPIView


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
    queryset = Interaction.objects.all()

class PartnerListView(ListAPIView):
    serializer_class = PartnerSerializer
    queryset = Partner.objects.all()

class InteractionByIDListView(ListAPIView):
    serializer_class = InteractionSerializer
    
    def get_queryset(self):
        #self.kwargs['partner_id']
        return Interaction.objects.filter(partner_id=self.kwargs['partner_id'])

