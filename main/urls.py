from django.urls import path
from main.views import CompanyListView,InteractionListView,PartnerListView

urlpatterns = [
    # path('test/', Home.as_view()),
    path('companies/', CompanyListView.as_view()),
    path('interactions/', InteractionListView.as_view()),
    path('partners/',PartnerListView.as_view())
    #
]
