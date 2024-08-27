from django.shortcuts import render
from http.client import HTTPResponse
from rest_framework.response import Response
from api.serializers import *
from api.models import *
from rest_framework import generics
from ast import literal_eval

# Create your views here.


class CategorieAPIView(generics.RetrieveAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

    def get(self, request, pk, format=None):
        try:
            item = Categorie.objects.get(pk=pk)
            serializer = CategoryGetSerializer(item)
            return Response(serializer.data)
        except Categorie.DoesNotExist:
            return Response(status=404)

    def put(self, request, pk, format=None):
        try:
            item = Categorie.objects.get(pk=pk)
        except Categorie.DoesNotExist:
            return Response(status=404)
        serializer = CategorieSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(CategoryGetSerializer(item).data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        try:
            item = Categorie.objects.get(pk=pk)
        except Categorie.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204) 
    

class CategorieAPIListView(generics.CreateAPIView):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

    def get(self, request, format=None):
        items = Categorie.objects.order_by('-pk')
        return Response(CategoryGetSerializer(items, many=True).data)

    def post(self, request, format=None):
        serializer = CategorieSerializer(data=request.data)
        if serializer.is_valid():
            ctg = serializer.save()
            return Response(CategoryGetSerializer(ctg).data, status=201)
        return Response(serializer.errors, status=400)


class ArticleByCategorieAPIListView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, pk, format=None):
        items = Article.objects.filter(categorie=pk)
        serializer = ArticleGetSerializer(items, many=True)
        return Response(serializer.data)


class ArticleAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, pk, format=None):
        try:
            item = Article.objects.get(pk=pk)
            serializer = ArticleGetSerializer(item)
            return Response(serializer.data)
        except Article.DoesNotExist:
            return Response(status=404)

    def put(self, request, pk, format=None):
        try:
            item = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=404)
        serializer = ArticleSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(ArticleGetSerializer(item).data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk, format=None):
        try:
            item = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            return Response(status=404)
        item.delete()
        return Response(status=204) 
    

class ArticleAPIListView(generics.CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, format=None):
        items = Article.objects.order_by('-pk')
        return Response(ArticleGetSerializer(items, many=True).data)

    def post(self, request, format=None):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            prdt = serializer.save()
            return Response(ArticleGetSerializer(prdt).data, status=201)
        return Response(serializer.errors, status=400)


class VenteAPIView(generics.CreateAPIView):
    permission_classes = ()
    queryset = Vente.objects.all()
    serializer_class = VenteSerializer

    def post(self, request, format=None):
        self.data = request.data.copy()
        if 'item_list' in request.data and request.data['item_list']:
            items = literal_eval(request.data['item_list'])
            ref = ""
            client = None
            if 'reference' in request.data and request.data['reference']:
                ref = request.data['reference']
            if 'client' in request.data and request.data['client']:
                client = User.objects.get(id=request.data['client'])
            vente = Vente.objects.create(reference=ref)
            vente.client = client
            vente.save()
            for el in items:
                article = Article.objects.get(id=el.get('article'))
                if article.quantite >= int(el.get('quantite')):
                    total = article.prix * int(el.get('quantite'))
                    detailSerializer = DetailVenteSerializer(
                        data={
                            "quantite": el.get('quantite'),
                            "prix": total,
                            "article": article.id,
                            })
                    if detailSerializer.is_valid():
                        detailSerializer.save()
                        vente.total += total
                        vente.quantite += int(el.get('quantite'))
                        vente.save()
                        vente.details.add(detailSerializer.data['id'])
                article.quantite = article.quantite - int(el.get('quantite'))
                article.save()
        return Response(VenteSerializer(vente).data)



class VenteAPIListView(generics.RetrieveAPIView):
    queryset = Vente.objects.all()
    serializer_class = VenteSerializer

    def get(self, request, format=None):
        items = Vente.objects.order_by('-pk')
        word = request.GET.get('word')
        if word:
            items = items.filter(reference=word)
        return Response(VenteSerializer(items, many=True).data)