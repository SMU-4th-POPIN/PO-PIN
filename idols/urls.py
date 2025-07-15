
from django.urls import path
from . import views

app_name = 'idols'

urlpatterns = [
    path("search/", views.idol_search_api, name="idol_search"), 
]