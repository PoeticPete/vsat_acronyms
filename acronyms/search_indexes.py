from elasticsearch_dsl import Document, Text, analyzer, tokenizer
from django.core.management.base import BaseCommand
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch_dsl import connections
import certifi
import csv

name_analyzer = analyzer('ngram_tokenizer_analyzer',
                         tokenizer=tokenizer('ngram_tokenizer', type='nGram', min_gram=1, max_gram=20),
                         filter=['lowercase']
                         )


class AcronymIndex(Document):
    id = Text()
    acronym = Text(term_vector="yes", analyzer=name_analyzer)
    definition = Text(analyzer=name_analyzer)

    class Index:
        name = 'acronyms'

# from elasticsearch_dsl import DocType, Text, analyzer, tokenizer, MetaField
#
#
# name_analyzer = analyzer('ngram_tokenizer_analyzer',
#                          tokenizer=tokenizer('ngram_tokenizer', type='nGram', min_gram=2, max_gram=20),
#                          filter=['lowercase']
#                          )
#
#
# # ngram_filter = token_filter('ngram_filter', type='nGram', min_gram=2, max_gram=20)
#
# class AcronymIndex(DocType):
#     id = Text()
#     acronym = Text(term_vector="yes", analyzer=name_analyzer)
#     definition = Text(term_vector="yes", analyzer=name_analyzer)
#     description = Text()
#
#     class Meta:
#         index = 'acronyms'
#         all = MetaField(type="text", analyzer="ngram_tokenizer_analyzer")
