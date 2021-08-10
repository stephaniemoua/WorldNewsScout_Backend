from ProjectRoot.settings import AZURE_SECRET_KEY
import requests
from ProjectAPI.models import Article, Country, Language, Sentiment, Source, SpotInstance, Topic


markets = ['en-AU', 'en-CA', 'en-GB', 'en-US']
country_set = {'en-US':"us", 'en-AU':'au', 'en-CA':'ca', 'en-GB':'gb'}
# locale = 'en-CA'

ACCESS_KEY = AZURE_SECRET_KEY
URL = 'https://api.bing.microsoft.com//v7.0/news/trendingtopics'
HEADERS = {"Ocp-Apim-Subscription-Key" : ACCESS_KEY}


def getTrendingTopics():
    for locale in markets:
        status = getTopicByCountry(locale)
    #status = getTopicByCountry(locale)
    return status

# Extracts trending topics in the news 
def getTopicByCountry(locale): 
    code = country_set.get(locale)
    country = Country.objects.get(countryId = code)

    # GET request to Bing News API 
    headers = {"Ocp-Apim-Subscription-Key" : ACCESS_KEY}
    params  = {"mkt": locale, "sortBy": "relevance"}
    response = requests.get(URL, headers=headers, params=params)
    data = response.json()      #deserialize response 

    count = 0
    max_topics = 10

    for obj in data["value"]:   # for each topic object in response
        count += 1
        topic = obj['name']             # get the TOPIC
        context = obj['query']['text']  # get the related SEARCH QUERY
        if (Topic.objects.filter(topic = topic).exists() != True): 
            if (len(topic) < 50) and (count <= max_topics):
            #if (count <= max_topics):
                print (topic + ': ' + context)
                Topic.objects.create(         # create a TOPIC object   
                    topic = topic,
                    context = context,
                    locale = country )
            
    return ('trendingTopic')

# descriptions = [article["description"] for article in search_results["value"]]