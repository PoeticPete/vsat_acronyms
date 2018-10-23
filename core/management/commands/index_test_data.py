from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections
from vsat_acronyms_backend.settings import ELASTIC_SEARCH_ROOT
from acronyms.search_indexes import AcronymIndex
import certifi


class Command(BaseCommand):
    help = 'flushes the conferences and topics indexes'

    def handle(self, *args, **options):
        print(ELASTIC_SEARCH_ROOT)
        connections.create_connection(hosts=[ELASTIC_SEARCH_ROOT])
        # es = Elasticsearch(ELASTIC_SEARCH_ROOT, use_ssl=True, ca_certs=certifi.where())
        es = Elasticsearch(ELASTIC_SEARCH_ROOT, ca_certs=certifi.where())

        es.indices.delete(index='acronyms', ignore=[400, 404])
        AcronymIndex.init()
