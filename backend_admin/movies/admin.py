from django.contrib import admin
from movies.models import Filmwork, FilmWorkGenre, FilmWorkPerson, Genre, Person


class PersonRoleInline(admin.TabularInline):
    model = FilmWorkPerson
    extra = 0


class GenreInline(admin.TabularInline):
    model = FilmWorkGenre
    extra = 0


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    # отображение полей в списке
    list_display = (
        "title",
        "type",
        "rating",
        "mpaa_age_rating",
        "creation_date",
        "updated_at",
    )

    # фильтрация в списке
    list_filter = ("rating", "mpaa_age_rating")

    # поиск по полям
    search_fields = ("title", "description", "id")

    # порядок следования полей в форме создания/редактирования
    fields = ("title", "type", "description", "file_path", "rating", "mpaa_age_rating")

    raw_id_fields = ("genres", "persons")

    inlines = [
        PersonRoleInline,
        GenreInline,
    ]


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name", "description")


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
