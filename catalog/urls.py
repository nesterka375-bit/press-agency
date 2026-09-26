from django.urls import path
from catalog.views import index, TopicListView

app_name = "catalog"
urlpatterns = [
    path("", index, name="index"),
    path("newspapers/", TopicListView.as_view(), name="topic_list"),
]
