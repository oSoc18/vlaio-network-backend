from django.urls import path
from main.views import CompanyListView,InteractionListView,PartnerListView,OverlapListView, DataFileView, OverlapTimeframeListView

urlpatterns = [
    # path('test/', Home.as_view()),
    path('companies/', CompanyListView.as_view()),
    path('interactions/', InteractionListView.as_view()),
    path('partners/',PartnerListView.as_view()),
    path('overlap/', OverlapListView.as_view()),
    path('upload/', DataFileView.as_view()),
    path('overlap/timeframe/', OverlapTimeframeListView.as_view())
]

