from django.urls import path
from catalog.views import index

app_name = "catalog"
urlpatterns = [
    path("", index, name="index"),
]

