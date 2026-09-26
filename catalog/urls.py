from django.urls import path
from catalog.views import index, TopicListView, TopicDetailView

app_name = "catalog"

urlpatterns = [
    path("", index, name="index"),
    path("newspapers/", TopicListView.as_view(), name="topic_list"),
    path(
        "topics/<str:name>/", TopicDetailView.as_view(), name="topic_detail"),
]
