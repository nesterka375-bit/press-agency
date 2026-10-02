from django.urls import path
from catalog.views import index, TopicListView, RedactorsListView, TopicDetailView, NewsDetailView

app_name = "catalog"

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic_list"),
	path("redactors/", RedactorsListView.as_view(), name="redactor_list"),
    path(
        "topics/<str:name>/", TopicDetailView.as_view(), name="topic_detail"),
	path("topics/<str:name>/<int:pk>/", NewsDetailView.as_view(), name="news_detail"),
]
