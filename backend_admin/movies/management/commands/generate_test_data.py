import random

from django.core.management.base import BaseCommand
from django.db import transaction
from movies.models import Filmwork, FilmWorkGenre, FilmWorkPerson, Genre, Person
from progress.bar import IncrementalBar

from factories import (
    FilmworkFactory,
    FilmWorkGenreFactory,
    FilmWorkPersonFactory,
    GenreFactory,
    PersonFactory,
)

NUM_GENRES = 1000
NUM_PERSON = 1000
NUM_FILMS = 10000


class Command(BaseCommand):
    help = "Создаем тестовые данные"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Удаляем старые данные...")
        models = [Person, Filmwork, FilmWorkPerson, FilmWorkGenre, Genre]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Создаем данные...")
        genres = self._generate_genres()
        persons = self._generate_persons()
        self._generate_fims(persons=persons, genres=genres)

    def _generate_persons(self):
        persons = []
        person_time = IncrementalBar("Persons", max=NUM_PERSON)
        for _ in range(NUM_PERSON):
            person = PersonFactory.build()
            persons.append(person)
            person_time.next()

        Person.objects.bulk_create(persons)
        return persons

    def _generate_genres(self):
        genres = []
        genres_time = IncrementalBar("Genres", max=NUM_GENRES)
        for _ in range(NUM_GENRES):
            genre = GenreFactory.build()
            genres.append(genre)
            genres_time.next()

        Genre.objects.bulk_create(genres)
        return genres

    def _generate_fims(self, persons, genres):
        films = []
        films_work_genre = []
        films_work_person = []
        film_time = IncrementalBar("Films", max=NUM_FILMS)
        for _ in range(NUM_FILMS):
            film = FilmworkFactory.build()
            films.append(film)

            person = random.choice(persons)
            genre = random.choice(genres)

            film_work_genre = FilmWorkGenreFactory.build(film_work=film, genre=genre)
            film_work_person = FilmWorkPersonFactory.build(
                film_work=film, person=person
            )

            films_work_genre.append(film_work_genre)
            films_work_person.append(film_work_person)
            film_time.next()

        Filmwork.objects.bulk_create(films)
        FilmWorkPerson.objects.bulk_create(films_work_person)
        FilmWorkGenre.objects.bulk_create(films_work_genre)
