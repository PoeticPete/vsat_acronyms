from rest_framework import generics
import logging
import json
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from elasticsearch_dsl import Search
from acronyms.serializers import AcronymSerializer
from acronyms.models import Acronym

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


# Create your views here.
class AcronymView(generics.ListAPIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        """
        Creates a new acronym

        :param request:
        :return:
        """

        json_body = {}
        if request.body != b'':
            json_body = json.loads(request.body.decode('utf-8'))

        acronym = json_body.get('acronym', None, )
        definition = json_body.get('definition', None, )

        if all((acronym, definition)):
            try:
                new_acronym = Acronym()

                for key in json_body:
                    if key == "id":
                        return JsonResponse({'status': "failed", 'error': "Not allowed to define acronym id"},
                                            status=400)

                    setattr(new_acronym, key, json_body[key])

                new_acronym.save()

                return JsonResponse(
                    AcronymSerializer(new_acronym, many=False, fields=request.GET.get('fields', )).data,
                    status=201)

            except BaseException as e:
                logging.debug(e)
                return JsonResponse({"error": "Unable to create acronym."},
                                    status=400)
        else:
            return JsonResponse({"error": "Unable to create acronym. Must include acronym and definition."},
                                status=400)


    def get(self, request, **kwargs):
        """
        search for a user
        :param request: the HTTP GET request
        :return: JSON
        """

        if "search_query" in request.GET:
            query = str(request.GET.get("search_query"))

            s = Search(index="acronyms").query("match", acronym=query)
            response = s.execute()

            logging.debug(response)

            hits_list = []
            for hit in response.to_dict()["hits"]["hits"]:
                hit = hit['_source']
                hits_list.append(hit)

            return JsonResponse({'data': hits_list})

        return JsonResponse({'status': "error", 'detail': "please include a query"}, status=400)
