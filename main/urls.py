from django.urls import path
from main.views import CompanyListView

urlpatterns = [
    # path('test/', Home.as_view()),
    path('companies/', CompanyListView.as_view()),
    #
]
