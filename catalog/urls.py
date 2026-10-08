from django.urls import path
from catalog.views import index, TopicListView, RedactorListView, AllNewsListView, TopicDetailView, RedactorDetailView, \
	NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView, approve_news

app_name = "catalog"

urlpatterns = [
    path("", index, name="index"),
    path("topics/", TopicListView.as_view(), name="topic_list"),
	path("redactors/", RedactorListView.as_view(), name="redactor_list"),
	path("all_news/", AllNewsListView.as_view(), name="all_news_list"),
    path("topics/<str:name>/", TopicDetailView.as_view(), name="topic_detail"),
	path("redactors/<str:username>/", RedactorDetailView.as_view(), name="redactor_detail"),
	path("topics/<str:name>/<int:pk>/", NewsDetailView.as_view(), name="news_detail"),
	path("news/create/", NewsCreateView.as_view(), name="news_create"),
	path("topics/<str:name>/<int:pk>/update/", NewsUpdateView.as_view(), name="news_update"),
    path("topics/<str:name>/<int:pk>/delete/", NewsDeleteView.as_view(), name="news_delete"),
    path("news/<int:pk>/approve/", approve_news, name="news_approve"),
]
