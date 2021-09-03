import logging

from elasticsearch import Elasticsearch

logger = logging.getLogger()


class ESLoader:
    def __init__(self):

        self.es = Elasticsearch(hosts="es")

    def load_to_es(self, records, index_name: str):
        logger.info(f"records {records}")
        self.es.bulk(body=records, index=index_name)
