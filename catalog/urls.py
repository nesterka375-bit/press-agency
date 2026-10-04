from django.urls import path
from catalog.views import index, TopicListView, RedactorListView, AllNewsListView, TopicDetailView, RedactorDetailView, NewsDetailView

app_name = "catalog"

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic_list"),
	path("redactors/", RedactorListView.as_view(), name="redactor_list"),
	path("allews/", AllNewsListView.as_view(), name="all_news_list"),
    path("topics/<str:name>/", TopicDetailView.as_view(), name="topic_detail"),
	path("redactors/<str:username>/", RedactorDetailView.as_view(), name="redactor_detail"),
	path("topics/<str:name>/<int:pk>/", NewsDetailView.as_view(), name="news_detail"),
]
