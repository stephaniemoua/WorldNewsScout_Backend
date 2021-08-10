from rest_framework import serializers
from .models import Language, Country, Source, Topic, Article, SpotInstance, Sentiment

# Components that convert models to JSON objects 
# and JSON objects to models 

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language 
        fields = ('languageId')
        
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country 
        fields = ('countryId','countryName')

class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source 
        fields = ('sourceId','sourceName', 'locale', 'language')

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model=Topic 
        fields = '__all__'

class SentimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentiment 
        fields = '__all__'

class ArticleSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Article 
        fields = ('url', 'title', 'author', 'description', 'urlToImage', 'publishedAt', 'content', 'fullDesc')
        read_only_fields = ('source', 'sentimentScore', 'keyword')

class SpotInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotInstance 
        fields = ('locale', 'spotNum', 'keyword')
