from django.db import models
from django.urls import reverse

# Create your models here.
# Models are data entities, or tables 
# To import: 
# from .models import Article, Country, Language, Sentiment, Source, SpotInstance, Topic


class Country(models.Model):
    countryId = models.CharField(max_length=2)
    countryName = models.CharField(max_length=50)

    def __str__(self):
        return self.countryId

class Language(models.Model):
    languageId = models.CharField (max_length=2, primary_key=True)

    def __str__(self):
        return self.languageId

class Sentiment(models.Model):
    mixed = models.CharField(max_length=50,default="0.0")
    positive = models.CharField(max_length=50,default="0.0")
    neutral = models.CharField(max_length=50,default="0.0")
    negative = models.CharField(max_length=50,default="0.0")
    sentiment = models.CharField(max_length=20, default='0')

    def __str__(self):
        return self.sentiment

class Source(models.Model):
    sourceId = models.CharField(max_length=50, primary_key=True)
    sourceName = models.CharField(max_length=50)
    locale = models.ForeignKey(Country, on_delete=models.CASCADE)
    language =  models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.sourceId

    def get_source_name(self):
        return self.sourceName

class Topic(models.Model):
    topic = models.TextField(default='DEFAULT_TOPIC', unique=True)
    context = models.TextField(default='', blank=True, null=True)
    locale = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    

    def get_topic(self):
        return self.topic

    def get_context(self):
        return self.context
    
    # def display_keyword(self):
    #     keywordList = self.term0 + ', ' + self.term2 + ', ' + self.term3 + ', ' + self.term4 + ', '
    #     keywordList += self.term5 + ', ' + self.term6 + ', ' +  self.term7 + ', ' + self.term8 + ', ' + self.term9
    #     return keywordList
    # display_keyword.short_description = 'Keyword'

class SpotInstance(models.Model):
    locale = models.ForeignKey(Country, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default=0)
    spotNum = models.IntegerField(null=False)
    keywords = models.TextField(default='')

class Article(models.Model):
    url = models.URLField (unique=True)
    title = models.TextField(default="DEFAULT_TITLE")
    author = models.CharField(max_length=50, blank= True, null=True)
    description = models.TextField(blank=True, null=True)
    urlToImage = models.URLField(blank=True, null=True)
    publishedAt = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    fullDesc = models.TextField(default='')
    source =  models.ForeignKey(Source, on_delete=models.CASCADE, default="DEFAULT_SOURCE_ID" )
    sentimentScore = models.ForeignKey(Sentiment, on_delete=models.CASCADE, default="DEFAULT_SENTIMENT_ID" )
    keyword = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ['publishedAt']

    def __str__(self):
        return self.title

    def get_source_id(self):
        return self.source.sourceId

    def get_source_fullDesc(self):
        return self.fullDesc

    def get_source_sentiment(self):
        return self.sentimentScore.sentiment

    def get_keyword(self):
        return self.keyword.topic

    def get_absolute_url(self):
        #Returns the url to access a detail record for this book.#
        return reverse('article-detail', args=[str(self.id)])
