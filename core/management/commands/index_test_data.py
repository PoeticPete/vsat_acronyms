from elasticsearch_dsl import Document, Text, analyzer, tokenizer
from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import connections
from vsat_acronyms_backend.settings import ELASTIC_SEARCH_ROOT
from acronyms.search_indexes import AcronymIndex
import certifi
import csv


def get_sheet_data():
    with open("result.csv", "rt", encoding="utf8") as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            if len(line) == 2:
                print(line[1])
                yield {
                    "_index": "acronyms",
                    "_type": "doc",
                    "acronym": line[0],
                    "definition": line[1]
                }


class Command(BaseCommand):
    help = 'reindexes the Elastic Search acronyms index '

    def handle(self, *args, **options):

        connections.create_connection(hosts=[ELASTIC_SEARCH_ROOT])
#        es = Elasticsearch(ELASTIC_SEARCH_ROOT, use_ssl=True, ca_certs=certifi.where())
        es = Elasticsearch(ELASTIC_SEARCH_ROOT)
        es.indices.delete(index='acronyms', ignore=[400, 404])

        AcronymIndex.init()

        bulk(es, get_sheet_data())
