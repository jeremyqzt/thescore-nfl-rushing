import csv
import json
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from stats.cqrs.queries import GetAllStatsQuery
from api.constants import SortTypesMap, SortByTypesMap, NoneInput


class NFLRushingView(APIView):
    def get(self, request):
        sort = SortTypesMap[request.query_params.get('sort', NoneInput)]
        sort_by = SortByTypesMap[request.query_params.get(
            'sort_by', NoneInput)]
        filter = request.query_params.get('filter', None)
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))

        output, total = GetAllStatsQuery().execute(sort_on=sort, sort_by=sort_by,
                                                   name_filter=filter, page=page, page_size=page_size)

        resp = {
            "data": output,
            "current": page,
            "total": total
        }
        return Response(resp, status=status.HTTP_200_OK)


class NFLRushingEXCLView(APIView):
    def post(self, request):
        post_data = json.loads(request.body.decode("utf-8"))
        sort = SortTypesMap[post_data.get('sort', NoneInput)]
        sort_by = SortByTypesMap[post_data.get(
            'sort_by', NoneInput)]
        filter = post_data.get('filter', None)

        output, _ = GetAllStatsQuery().execute(sort_on=sort, sort_by=sort_by,
                                               name_filter=filter, page=0, page_size=0)

        response = HttpResponse(
            content_type='text/csv',
            headers={
                'Content-Disposition': 'attachment; filename="export.csv"'},
        )

        csv_columns = ["Player",
                       "Team",
                       "Pos",
                       "Att",
                       "Att/G",
                       "Yds",
                       "Avg",
                       "Yds/G",
                       "TD",
                       "Lng",
                       "1st",
                       "1st%",
                       "20+",
                       "40+",
                       "FUM", ]

        writer = csv.DictWriter(response, fieldnames=csv_columns)
        writer.writeheader()
        for data in output:
            # Return type is a tuple of 1
            writer.writerow(data)

        return response
