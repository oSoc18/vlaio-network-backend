from django.shortcuts import render
from .models import Company, Interaction,Partner, Overlap, InteractionsLevels
from .serializers import CompanySerializer, InteractionSerializer, PartnerSerializer, OverlapSerializer, InteractionsLevelsSerializer
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


class InteractionsLevelsListView(ListAPIView):
    serializer_class = InteractionsLevelsSerializer
    queryset = InteractionsLevels.objects.all()


###############################################################################


class OverlapListView(ListAPIView):
    serializer_class = OverlapSerializer
    queryset = Overlap.objects.all()
    