from django.contrib import admin
from .models import Article, Country, Language, Sentiment, Source, SpotInstance, Topic


# Register your models here.
class AppAdmin(admin.ModelAdmin):
    # Language
    list = ('languageId') 


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'sentimentScore', 'fullDesc')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('countryId','countryName')

class SentimentAdmin(admin.ModelAdmin):
    list_display = ('sentiment', 'mixed', 'positive', 'negative', 'neutral')

class SourceAdmin(admin.ModelAdmin):
    list_display = ('sourceId', 'sourceName', 'locale')

class SpotInstanceAdmin(admin.ModelAdmin):
    list_display = ('locale', 'spotNum', 'topic', 'keywords')

class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_topic', 'get_context')

# Display full list of Models' fields
admin.site.register(Language, AppAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Sentiment, SentimentAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(SpotInstance, SpotInstanceAdmin)
admin.site.register(Topic,TopicAdmin)








