from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from catalog.forms import NewsForm
from catalog.models import Newspaper, Topic, Redactor

@login_required
def index(request: HttpRequest) -> HttpResponse:
    latest_posts = Newspaper.objects.select_related("topic").prefetch_related(
        "publishers"
    )[:5]

    context = {
        "latest_posts": latest_posts,
    }
    return render(request, "catalog/index.html", context=context)

class TopicListView(LoginRequiredMixin,generic.ListView):
    model = Topic
    template_name = "catalog/topic_list.html"
    context_object_name = "topics"

    def get_queryset(self):
        return Topic.objects.annotate(
            newspapers_count=Count("newspapers")
        ).order_by("name")


class RedactorListView(LoginRequiredMixin, generic.ListView):
    model = Redactor
    template_name = "catalog/redactor_list.html"
    context_object_name = "redactors"

    def get_queryset(self):
        return (
            Redactor.objects.exclude(username="admin")
            .annotate(newspapers_count=Count("newspapers"))
            .order_by("username")
        )


class AllNewsListView(LoginRequiredMixin, generic.ListView):
    model = Newspaper
    template_name = "catalog/all_news_list.html"
    context_object_name = "newspapers"
    slug_field = "name"
    slug_url_kwarg = "name"


class TopicDetailView(LoginRequiredMixin, generic.DetailView):
    model = Topic
    template_name = "catalog/topic_detail.html"
    context_object_name = "topic"
    slug_field = "name"
    slug_url_kwarg = "name"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("newspapers__publishers")

    def get_object(self, queryset=None):
        name = self.kwargs.get("name")
        topic = Topic.objects.filter(name__iexact=name).first()
        if not topic:
            for t in Topic.objects.all():
                if t.name.lower() == name.lower():
                    topic = t
                    break
        return get_object_or_404(
            Topic.objects.filter(pk=topic.pk) if topic else Topic.objects.none()
        )


class RedactorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Redactor
    template_name = "catalog/redactor_detail.html"
    context_object_name = "redactor"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("newspapers__topic", "newspapers__publishers")
        )

    def get_object(self, queryset=None):
        username = self.kwargs.get("username")
        return get_object_or_404(Redactor, username__iexact=username)


class NewsDetailView(LoginRequiredMixin, generic.DetailView):
    model = Newspaper
    template_name = "catalog/news_detail.html"
    context_object_name = "news"

    def get_queryset(self):
        return super().get_queryset().select_related("topic").prefetch_related("publishers")


class NewsCreateView(LoginRequiredMixin, generic.CreateView):
  model = Newspaper
  form_class = NewsForm
  template_name = "catalog/news_form.html"

  def get_success_url(self):
      return reverse(
          "catalog:news_detail",
          kwargs={"name": self.object.topic.name.lower(), "pk": self.object.pk},
      )


class NewsUpdateView(LoginRequiredMixin, generic.UpdateView):
  model = Newspaper
  form_class = NewsForm
  template_name = "catalog/news_form.html"

  def get_success_url(self):
    return reverse_lazy(
        "catalog:news_detail",
        kwargs={"name": self.object.topic.name.lower(), "pk": self.object.pk},
    )

  def access(self):
      newspaper = self.get_object()
      user = self.request.user
      return (
              user.is_staff
              or user.is_superuser
              or newspaper.publishers.filter(pk=user.pk).exists()
      )


class NewsDeleteView(LoginRequiredMixin, generic.DeleteView):
  model = Newspaper
  template_name = "catalog/news_confirm_delete.html"
  success_url = reverse_lazy("catalog:all_news_list")

  def access(self):
      newspaper = self.get_object()
      user = self.request.user
      return (
              user.is_staff
              or user.is_superuser
              or newspaper.publishers.filter(pk=user.pk).exists()
      )


@permission_required("catalog.change_newspaper")
def approve_news(request, pk):
  news = get_object_or_404(Newspaper, pk=pk)
  news.is_approved = True
  news.save()
  return redirect(
      "catalog:news_detail", name=news.topic.name.lower(), pk=news.pk
  )

