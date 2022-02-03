from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from bs4 import BeautifulSoup
from .serializers import ItemModelSerializer
from .models import Item


class ExtractWords(APIView):

    def post(self, request):
        try:
            data = request.data
            if "url" not in data:
                return Response({"success": False, "err": "Pass the URL"}, status=400)
            data = requests.get(data["url"])
            text = data.text
            soup = BeautifulSoup(text, features="html.parser")
            for script in soup(["script", "style"]):
                script.decompose()
            strips = list(soup.stripped_strings)
            added = 0
            for word in strips:
                if Item.objects.filter(name=word).count() == 0:
                    Item.objects.create(name=word)
                    added += 1
            return Response({"success": True, "msg": f"{added} records fetched"}, status=200)
        except:
            return Response({"success": False, "err": "Internal server error"}, status=500)



class SearchWord(APIView):
    
    def get(self, request):
        params = request.query_params
        if "q" not in params:
            return Response({"success": False, "err": "Pass the URL"}, status=400)
        data = Item.objects.filter(name__istartswith=params["q"]).all()
        serializer = ItemModelSerializer(data, many=True)
        return Response({"success": True, "msg": serializer.data}, status=200)
