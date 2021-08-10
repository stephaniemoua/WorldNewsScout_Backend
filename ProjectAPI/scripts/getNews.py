from ProjectRoot.settings import APIKEY
import requests
from ProjectAPI.models import Article, Country, Language, Sentiment, Source, SpotInstance, Topic
import datetime

########## VARIABLES ######### 
COUNTRY_LIST = ["us", "ca", "gb", "au"]
LANGUAGE = 'en'
PAGE_SIZE = '5'
SORT_BY = 'publishedAt'


def getTimeRange():
    dateX = datetime.date.today() - datetime.timedelta(days=7)
    return dateX.isoformat() 


###### NEWSAPI.ORG INTERACTION ######

# defines URL to send to NewsAPI.org and calls saveArticles()
# no keyword provided 
def getNewsAuto():
    # Time period (last 24hrs) to identify articles to retrieve
    time_limit = getTimeRange()

    # get all sources 
    # process for each source
    allSources = Source.objects.all()
    for item in allSources:
        source = item.get_source_name()
        url = "https://newsapi.org/v2/everything?pageSize={}&sortBy={}&language={}&from={}&sources={}&apiKey={}".format(
                PAGE_SIZE, SORT_BY, LANGUAGE, time_limit, item, APIKEY)
        status = saveArticles2(url)

    return status


# updated URL with keyword provided
def getNews(search):
    # Time period (last 24hrs) to identify articles to retrieve
    time_limit = getTimeRange()

    # create a topic card 
    if (Topic.objects.filter(topic = search).exists() != True): 
        topic_object = Topic.objects.create(topic = search)
    else:
        topic_object = Topic.objects.get(topic = search)

    # get all sources 
    # process for each source
    allSources = Source.objects.all()
    for item in allSources:
        source = item.get_source_name()
        url = "https://newsapi.org/v2/everything?q={}&pageSize={}&sortBy={}&language={}&from={}&sources={}&apiKey={}".format(
                search, PAGE_SIZE, SORT_BY, LANGUAGE, time_limit, item, APIKEY)
        status = saveArticles(url, topic_object)
    return status

###### DATABASE INTERACTION ######
# read the response from NewsAPI.org endpoints 
# deserialize elements into Article objects 
# save/create Article objects in the database
def saveArticles(url, topic_object):
    r = requests.get(url=url)
    data = r.json() #read the json file 

    if data["status"] != "ok":
        return 'Failed - Articles not saved'

    for obj in data['articles']:
        source_temp = obj['source']['name']

        # save if article from list of sources
        if (Source.objects.filter(sourceName = source_temp).exists()): 
            url_temp = obj['url']

            # avoid dupliate based on URL 
            if (Article.objects.filter(url = url_temp).exists() != True): 
                Article.objects.create(
                url = obj['url'],
                title = obj['title'],
                author = obj['author'],
                description = obj['description'],
                urlToImage = obj['urlToImage'],
                publishedAt = obj['publishedAt'],
                content = obj['content'],
                keyword = topic_object,
                source = Source.objects.get(sourceName = source_temp),
                sentimentScore = Sentiment.objects.create()
            )
    
    # return HttpResponse(result) # returns array of articles saved to db, for testing
    return 'Success - Articles Saved'


def saveArticles2(url):
    r = requests.get(url=url)
    data = r.json() #read the json file 

    if data["status"] != "ok":
        return 'Failed - Articles not saved'

    for obj in data['articles']:
        source_temp = obj['source']['name']

        # save if article from list of sources
        if (Source.objects.filter(sourceName = source_temp).exists()): 
            url_temp = obj['url']

            # avoid dupliate based on URL 
            if (Article.objects.filter(url = url_temp).exists() != True): 
                Article.objects.create(
                url = obj['url'],
                title = obj['title'],
                author = obj['author'],
                description = obj['description'],
                urlToImage = obj['urlToImage'],
                publishedAt = obj['publishedAt'],
                content = obj['content'],
                source = Source.objects.get(sourceName = source_temp),
                sentimentScore = Sentiment.objects.create()
            )
    
    # return HttpResponse(result) # returns array of articles saved to db, for testing
    return 'Success - Articles Saved'