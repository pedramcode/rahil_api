from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
from .serializers import ItemModelSerializer
from .models import Item
from . import data as cities_data


class Reset(APIView):

    def put(self, request):
            r_data = request.data
            if "password" not in r_data or r_data["password"] != "Pedi#0098":
                return Response({"success": False, "err": "Unauthorized"}, status=401)
            Item.objects.all().delete()
            for row in cities_data:
                name = row["Name"].lower()
                Item.objects.create(name=name)
            return Response({"success": True, "msg": f"Done"}, status=200)



class SearchWord(APIView):
    
    def get(self, request):
        params = request.query_params
        if "q" not in params:
            return Response({"success": False, "err": "Pass the URL"}, status=400)
        data = Item.objects.filter(name__istartswith=params["q"]).all()
        serializer = ItemModelSerializer(data, many=True)
        return Response({"success": True, "msg": serializer.data}, status=200)
