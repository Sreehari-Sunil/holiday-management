from django.urls import re_path
from . import views

app_name = "api_v1_holidays"

urlpatterns = [
   re_path(r"^$", views.get_holidays, name="list"),
   re_path(r"^get-detail/$", views.holidayDetail, name="detail"),
]