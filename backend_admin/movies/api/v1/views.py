from dataclasses import asdict, dataclass
from http import HTTPStatus
from typing import List, Optional

from django.contrib.postgres.aggregates import ArrayAgg
from django.core.exceptions import ValidationError
from django.db.models import Q, QuerySet
from django.http import JsonResponse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from movies.models import Filmwork


@dataclass
class MovieListResult:
    count: int
    total_pages: int
    prev: Optional[int]
    next: Optional[int]
    results: List


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ["get"]

    def get_queryset(self):
        actors = ArrayAgg(
            "persons__name",
            filter=Q(filmworkperson__role__exact="ACTOR"),
            distinct=True,
        )
        directors = ArrayAgg(
            "persons__name",
            filter=Q(filmworkperson__role__exact="WRITER"),
            distinct=True,
        )
        writers = ArrayAgg(
            "persons__name",
            filter=Q(filmworkperson__role__exact="DIRECTOR"),
            distinct=True,
        )

        queryset = (
            super()
            .get_queryset()
            .prefetch_related("genres", "persons")
            .values()
            .annotate(genres=ArrayAgg("genres__name", distinct=True))
            .annotate(actors=actors, writers=writers, directors=directors)
        )
        return queryset

    def render_to_response(self, context, **response_kwargs):
        if context is None:
            return JsonResponse(
                {
                    "status_code": HTTPStatus.NOT_FOUND,
                    "error": "The resource was not found",
                },
                status=HTTPStatus.NOT_FOUND,
            )
        return JsonResponse(context, safe=False)


class MoviesListApi(MoviesApiMixin, ListView):

    ordering = ["title"]
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        paginator = context["paginator"]
        page = context["page_obj"]

        prev_page = page.previous_page_number() if page.has_previous() else None
        next_page = page.next_page_number() if page.has_next() else None

        film_works: QuerySet = context["object_list"]

        return asdict(
            MovieListResult(
                count=paginator.count,
                total_pages=paginator.num_pages,
                prev=prev_page,
                next=next_page,
                results=list(film_works),
            )
        )


class MoviesDetailApi(MoviesApiMixin, DetailView):
    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except ValidationError:
            return None

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)["object"]
