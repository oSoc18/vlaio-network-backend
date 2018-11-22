from django.urls import path
from main.views import (
    CompanyListView, InteractionListView,
    PartnerListView, OverlapListView,
    DataFileView, InteractionTypeListView,
    view, apply_datafile, CompanyView)

urlpatterns = [
    # path('test/', Home.as_view()),
    # TODO: only ids ?
    path('companies/', CompanyListView.as_view()),
    path('companies/<pk>/interactions', CompanyView.as_view()),
    path('interactions/', InteractionListView.as_view()),
    path('interactions/types/', InteractionTypeListView.as_view()),
    path('partners/',PartnerListView.as_view()),
    path('overlap/', OverlapListView.as_view()),
    path('upload/', DataFileView.as_view()),
    path('apply/<int:id>', apply_datafile),
    path('view/', view)
]

