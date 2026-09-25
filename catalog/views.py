from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from catalog.models import Newspaper


def index(request: HttpRequest) -> HttpResponse:
	latest_posts = Newspaper.objects.select_related("topic").prefetch_related("publishers")[:5]

	context = {
		"latest_posts": latest_posts,
	}
	return render(request, "catalog/index.html", context=context)
