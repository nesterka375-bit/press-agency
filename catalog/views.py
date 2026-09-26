from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from catalog.models import Newspaper, Topic


def index(request: HttpRequest) -> HttpResponse:
    latest_posts = Newspaper.objects.select_related("topic").prefetch_related(
        "publishers"
    )[:5]

    context = {
        "latest_posts": latest_posts,
    }
    return render(request, "catalog/index.html", context=context)

class TopicListView(generic.ListView):
    model = Topic
    template_name = "catalog/topic_list.html"
    context_object_name = "topics"

    def get_queryset(self):
        return Topic.objects.annotate(
            newspapers_count=Count("newspapers")
        ).order_by("name")
