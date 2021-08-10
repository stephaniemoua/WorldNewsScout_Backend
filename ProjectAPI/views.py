from django.shortcuts import render
from django.core import serializers
from .serializers import ArticleSerializer, CountrySerializer, LanguageSerializer, SentimentSerializer, SourceSerializer, TopicSerializer, SpotInstanceSerializer
from .models import Article, Country, Language, Sentiment, Source, SpotInstance, Topic
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse

from ProjectAPI.scripts.getSentimentAnalysis import getSentimentAnalysis
from ProjectAPI.scripts.getTrendingTopics import getTrendingTopics
from ProjectAPI.scripts.getNews import getNews, getNewsAuto
from ProjectAPI.scripts.getDescriptions import getDescriptions

# Create your views here. Views are the functions 
# return list of topics > trending worlwide  
# return list of topcs > each country 



class LanguageViewSet (viewsets.ModelViewSet):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()

class CountryViewSet (viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()

class SourceViewSet (viewsets.ModelViewSet):
    serializer_class = SourceSerializer
    queryset = Source.objects.all()
    
    @action(detail=True)
    def source_details(self, request, pk=None):
        source = self.get_object()
        return Response(source)

class TopicViewSet (viewsets.ModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()

class SentimentViewSet (viewsets.ModelViewSet):
    serializer_class = SentimentSerializer
    queryset = Sentiment.objects.all()

class ArticleViewSet (viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()

    @action(detail=True)
    def article_details(self, request, pk=None):
        article = self.get_object()
        return Response(article)

class SpotInstanceViewSet (viewsets.ModelViewSet):
    serializer_class = SpotInstanceSerializer
    queryset = SpotInstance.objects.all()

    @action(detail=True)
    def spot_details(self, request, pk=None):
        spot = self.get_object()
        return Response(spot)

# Set the time frame to fetch articles 
# Retrieves articles using NewsAPI.org and saves articles to database  
def main(request, search='None'):

    # get topics  
    status = getTrendingTopics()

    # # get and save news Articles 
    if search is None: 
        status = getNewsAuto()     # retrieves and saves news articles to database

    else: 
        status = getNews(search)

    # Add the full description to each Article object  
    status = getDescriptions()

    # Add sentiment analysis to each Article object
    status = getSentimentAnalysis()
 
    return HttpResponse(status)

#################################################################
####################### HELPER METHODS ##########################


