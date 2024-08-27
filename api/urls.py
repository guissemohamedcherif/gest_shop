from django.contrib import admin
from django.urls import re_path
from api import views

urlpatterns = [

    # Endpoint des catégories
    re_path(r'^categories/$', views.CategorieAPIListView.as_view()),
    re_path(r'^categories/(?P<pk>[0-9]+)/$', views.CategorieAPIView.as_view()),
    
    # Endpoint de la liste des articles pour une catégorie donnée
    re_path(r'^categorie/(?P<pk>[0-9]+)/articles/$', views.ArticleByCategorieAPIListView.as_view()),

    # Endpoint des articles
    re_path(r'^articles/$', views.ArticleAPIListView.as_view()),
    re_path(r'^articles/(?P<pk>[0-9]+)/$', views.ArticleAPIView.as_view()),

    # Endpoint d'ajout d'une vente avec plusieurs produits 
    re_path(r'^add_vente/$', views.VenteAPIView.as_view()),

    # Endpoint de la liste des ventes 
    re_path(r'^ventes/$', views.VenteAPIListView.as_view()),

    # Endpoint d'export des ventes
    re_path(r'^export_ventes/$', views.ExportVenteCsv.as_view()),
]