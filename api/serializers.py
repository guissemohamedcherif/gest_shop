from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from api.models import *
from django.db.models import Q

class CategorieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categorie
        fields = '__all__'


class CategoryGetSerializer(serializers.ModelSerializer):
    parent = CategorieSerializer()
    product_count = serializers.SerializerMethodField("get_product_count")
    
    def get_product_count(self,obj):
        categories = Categorie.objects.exclude(id=obj.id)
        categorie = Categorie.objects.get(id=obj.id)
        ctg_list = []
        temoin_asc = categorie
        if categorie.parent:   
            while temoin_asc.parent:
                for ctg in categories:
                    if ctg == temoin_asc.parent:
                        temoin_asc = ctg 
                        ctg_list.append(temoin_asc.id)
        else:
            temoin_desc = categorie
            while temoin_desc.id in categories.values_list('parent', flat=True):
                for ctg in categories:
                    ctg.parent = temoin_desc
                    temoin_desc = ctg
                    ctg_list.append(temoin_desc.id)
        articles = Article.objects.filter(Q(categorie__id__in=ctg_list) | Q(categorie__id=categorie.id))
        return articles.count()

    class Meta:
        model = Categorie
        fields = ('id', 'nom', 'description', 'product_count', 'parent')


class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'


class ArticleGetSerializer(serializers.ModelSerializer):
    categorie = CategorieSerializer()

    class Meta:
        model = Article
        fields = '__all__'


class DetailVenteSerializer(serializers.ModelSerializer):

    class Meta:
        model = DetailVente
        fields = '__all__'


class VenteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vente
        fields = '__all__'