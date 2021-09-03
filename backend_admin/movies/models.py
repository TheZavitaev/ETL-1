from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.fields import AutoCreatedField, AutoLastModifiedField
from model_utils.models import UUIDModel


class TimeStampedMixin(models.Model):
    created_at = AutoCreatedField(_("создано"))
    updated_at = AutoLastModifiedField(_("обновлено в последний раз"))

    class Meta:
        abstract = True


class Genre(UUIDModel, TimeStampedMixin):
    name = models.CharField(_("название"), max_length=255)
    description = models.TextField(_("описание"), blank=True, null=True)

    class Meta:
        db_table = "genre"
        verbose_name = _("жанр")
        verbose_name_plural = _("жанры")

    def __str__(self):
        return self.name


class Person(UUIDModel, TimeStampedMixin):
    name = models.CharField(_("имя"), max_length=255)

    class Meta:
        db_table = "person"
        verbose_name = _("персона")
        verbose_name_plural = _("персоны")

    def __str__(self):
        return self.name


class FilmworkType(models.TextChoices):
    MOVIE = "MOVIE", _("фильм")
    SERIES = "SERIES", _("сериал")
    TV_SHOW = "TV_SHOW", _("тв шоу")


class MPAA_AgeRatingType(models.TextChoices):
    G = "general", _("без ограничений")
    PG = "parental_guidance", _("рекомендовано смотреть с родителями")
    PG_13 = "parental_guidance_strong", _("просмотр не желателен детям до 13 лет")
    R = "restricted", _("до 17 в сопровождении родителей")
    NC_17 = "no_one_17_under", _("только с 18")


class RoleType(models.TextChoices):
    ACTOR = "ACTOR", _("актер")
    WRITER = "WRITER", _("сценарист")
    DIRECTOR = "DIRECTOR", _("режиссер")


class Filmwork(UUIDModel, TimeStampedMixin):

    title = models.CharField(_("название"), max_length=254)
    description = models.TextField(_("описание"), blank=True, null=True)
    creation_date = models.DateField(_("дата создания фильма"), blank=True, null=True)
    rating = models.FloatField(
        _("рейтинг"), validators=[MinValueValidator(0)], blank=True
    )
    mpaa_age_rating = models.CharField(
        _("возрастной рейтинг"),
        choices=MPAA_AgeRatingType.choices,
        null=True,
        max_length=50,
    )
    imdb_rating = models.FloatField(
        _("рейтинг"), validators=[MinValueValidator(0)], default=0
    )
    type = models.CharField(
        _("тип"),
        max_length=20,
        choices=FilmworkType.choices,
        default=FilmworkType.MOVIE,
    )
    file_path = models.FileField(_("файл"), upload_to="film_works", blank=True)
    genres = models.ManyToManyField(
        Genre, blank=True, through="FilmWorkGenre", related_name="film_works"
    )
    persons = models.ManyToManyField(
        Person, blank=True, through="FilmWorkPerson", related_name="film_works"
    )

    class Meta:
        db_table = "film_work"
        verbose_name = _("кинопроизведение")
        verbose_name_plural = _("кинопроизведения")

    def __str__(self):
        return self.title


class FilmWorkPerson(UUIDModel):
    role = models.CharField(_("профессия"), choices=RoleType.choices, max_length=255)
    film_work = models.ForeignKey(
        Filmwork, on_delete=models.deletion.CASCADE, verbose_name=_("фильм")
    )
    person = models.ForeignKey(
        Person, on_delete=models.deletion.CASCADE, verbose_name=_("человек")
    )

    def __str__(self):
        return f"{self.person} in {self.film_work} as {self.role}"

    class Meta:
        db_table = "film_work_person"
        verbose_name = _("участник фильма")
        verbose_name_plural = _("участники фильмов")
        unique_together = ("film_work", "person", "role")


class FilmWorkGenre(UUIDModel):
    film_work = models.ForeignKey(
        Filmwork, on_delete=models.deletion.CASCADE, verbose_name=_("фильм")
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.deletion.CASCADE, verbose_name=_("жанр")
    )

    class Meta:
        db_table = "film_work_genre"
        verbose_name = _("жанр")
        verbose_name_plural = _("жанры")
        unique_together = ("film_work", "genre")
