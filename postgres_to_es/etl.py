import os
import json
import logging
from urllib3.exceptions import HTTPError
from time import sleep
from typing import Generator

import backoff
import psycopg2
from elasticsearch.exceptions import ElasticsearchException
from psycopg2.extensions import connection as _connection
from psycopg2.extras import RealDictCursor
from redis import Redis
from elasticsearch import Elasticsearch

from utils import EnhancedJSONEncoder, coroutine
from models import Movie
from state import RedisStorage

logger = logging.getLogger()

class ETL:
    def __init__(self, conn: _connection, storage: RedisStorage):
        self.conn = conn
        self.cursor = pg_conn.cursor(name='etl', cursor_factory=RealDictCursor)
        self.storage = storage
        self.es = Elasticsearch(hosts="es")
        # Размер пакетного запроса
        self.batch_size = 10

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(ElasticsearchException, HTTPError),
        max_tries=10,
    )

    @backoff.on_exception(backoff.expo, BaseException)
    def start(self, target):
        logger.info("started")
        while True:
            target.send(1)
            sleep(0.1)

    @coroutine
    def extract(self, target: Generator) -> Generator:
        while _ := (yield):
            SQL = """
                    WITH movies AS (
                            SELECT
                            id, 
                            title, 
                            description, 
                            rating, 
                            type,
                            imdb_rating,
                            updated_at 
                        FROM film_work
                        LIMIT 100
                    )
                    SELECT
                        fw.id, 
                        fw.title, 
                        fw.description, 
                        fw.rating, 
                        fw.type,
                        fw.imdb_rating,
                        fw.updated_at,
                        CASE
                            WHEN pfw.role = 'ACTOR' 
                            THEN ARRAY_AGG(jsonb_build_object('id', p.id, 'name', p.name))
                        END AS actors,
                        CASE
                            WHEN pfw.role = 'WRITER' 
                            THEN ARRAY_AGG(jsonb_build_object('id', p.id, 'name', p.name))
                        END AS writers,
                        CASE
                            WHEN pfw.role = 'DIRECTOR' 
                            THEN ARRAY_AGG(jsonb_build_object('id', p.id, 'name', p.name))
                        END AS directors,
                        ARRAY_AGG(g.name) AS genres
                        FROM movies as fw
                        LEFT JOIN film_work_person pfw ON pfw.film_work_id = fw.id
                        LEFT JOIN person p ON p.id = pfw.person_id
                        LEFT JOIN film_work_genre gfw ON gfw.film_work_id = fw.id
                        LEFT JOIN genre g ON g.id = gfw.genre_id
                        GROUP BY
                            fw.id, 
                            fw.title, 
                            fw.description, 
                            fw.rating, 
                            fw.type,
                            fw.imdb_rating,
                            fw.updated_at,
                            pfw.role
                        ORDER BY fw.updated_at
                """

            state = self.storage.retrieve_state()
            self.cursor.execute(SQL, (state,))

            count = 0
            while True:
                data = self.cursor.fetchmany(self.batch_size)
                if not data:
                    break

                target.send(data)



    @coroutine
    def transform(self, target: Generator) -> Generator:
        while result := (yield):
            transformed = []
            for row in result:
                movie = Movie.from_dict({**row})
                transformed.append(movie)

            target.send(transformed)

    @backoff.on_exception(
        wait_gen=backoff.expo,
        exception=(ElasticsearchException, HTTPError),
        max_tries=10,
    )
    @coroutine
    def load(self) -> Generator:
        while transformed := (yield):

            if len(transformed) == 0:
                continue

            movies_to_es = []
            for row in transformed:
                movies_to_es.extend(
                    [
                        json.dumps({"index": {"_index": "movies", "_id": row.id}}),
                        json.dumps(row, cls=EnhancedJSONEncoder),
                    ]
                )

            prepare_data = "\n".join(movies_to_es) + "\n"
            logger.info(f"records {prepare_data}")
            self.es.bulk(body=prepare_data, index="movies")
            storage.save_state(transformed[0].updated_at)

    def __call__(self, *args, **kwargs):
        load = self.load()
        transform = self.transform(load)
        extract = self.extract(transform)
        self.start(extract)


if __name__ == "__main__":
    dsl = {
        "dbname": os.getenv("POSTGRES_DB_NAME", "postgres"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "@J2JqrPRYoFnVv2jvV"),
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "options": "-c search_path=public,postgres",
    }
    try:
        with psycopg2.connect(**dsl) as pg_conn:
            redis_adapter = Redis(host="redis")
            storage = RedisStorage(redis_adapter=redis_adapter)
            etl = ETL(conn=pg_conn, storage=storage)
            etl()
    except psycopg2.DatabaseError as error:
        logger.info(f"Database error {error}")
    finally:
        pg_conn.close()