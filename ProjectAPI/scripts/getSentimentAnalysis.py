from ..models import Article, Sentiment
from ProjectRoot.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION
import boto3
import requests 
from django.http import HttpResponse
from rest_framework.response import Response
from bs4 import BeautifulSoup


LANGUAGE = 'en'

###### AWS SENTIMENT ANALYSIS ######

### MAIN FUNCTION ###
def getSentimentAnalysis():
    LANG = "en"
    # get all articles with empty SentimentScore
    articles_analysis = Article.objects.filter(sentimentScore__sentiment = "0")
    report = ''
    # process each article to get sentiment and save it 
    for article in articles_analysis: 
        desc = article.fullDesc        # retrieve full description 

        if len(desc.encode('utf-8')) > 5000:
            report = splitStringSentiment(article)

        if desc == "ErrorExtraction": 
            report = "skipped"

        else: 
            report = extractSentiment(article)

    return report

def extractSentiment(article): 
    desc = article.fullDesc

    try:           
        report = "Success sentiment"
        data = detectSentiment(desc, LANGUAGE)  # retrieve AWS results 
        # get Sentiment object connected to this Article by ID
        sentiment_id = article.sentimentScore.id
        # retrieve the specific Sentiment instance
        temp_sentiment = Sentiment.objects.get(id = sentiment_id)
        # update each field with correct info
        temp_sentiment.mixed = data["SentimentScore"]["Mixed"]
        temp_sentiment.positive = data["SentimentScore"]["Positive"]
        temp_sentiment.neutral = data["SentimentScore"]["Neutral"]
        temp_sentiment.negative = data["SentimentScore"]["Negative"]
        temp_sentiment.sentiment = data["Sentiment"]
        temp_sentiment.save(update_fields=['mixed', 'positive', 'negative', 'neutral', 'sentiment'])
            
    except: 
        report = "Failed - Sentiment not added"
            
    finally: 
        report = "Success - Sentiment saved"

    return report

# restrictions: 
# fulldesc must be < 5000 bytes 
# if text == error, don't process 
def detectSentiment(text, language):
    comprehend = boto3.client('comprehend', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)
    try: 
        response = comprehend.detect_sentiment(Text=text, LanguageCode=language)
    except: 
        response = HttpResponse(400)
    finally:     
        return response

def splitStringSentiment(article):
    mixedResults = []              # int
    positiveResults = []           # int
    neutralResults = []            # int
    negativeResults = []           # int

    # split fullDesc
    desc = article.fullDesc
    maxSize = 5000   # maximum byte size per segment
    stringSegments = [desc[i:i+maxSize] for i in range(0, len(desc), maxSize)] # array of string segments
    n = len(stringSegments)     # number of segments 

    # detect sentiment for each segment and save to arrays 
    for segment in stringSegments:
        
        data = detectSentiment(segment, LANGUAGE)  # retrieve AWS results 

        try: 
            # update each field with correct info
            mixedResults.append(data["SentimentScore"]["Mixed"]),
            positiveResults.append(data["SentimentScore"]["Positive"]),
            neutralResults.append(data["SentimentScore"]["Neutral"]),
            negativeResults.append(data["SentimentScore"]["Negative"])
        except: 
            report = "Failed - Sentiment not added"
            
        finally: 
            report = "Success - Sentiment saved"
            

    # get average of each field
    positive = sum(positiveResults) / n 
    negative = sum(negativeResults) / n 
    neutral = sum(neutralResults) / n 
    mixed = sum(mixedResults) / n

    # determine overall sentiment 
    options = {'POSITIVE': positive, 'NEGATIVE': negative, 'NEUTRAL': neutral, 'MIXED': mixed}  # dictionary
    results = [positive, negative, neutral, mixed]  # array to sort 
    results.sort(reverse=True)  # sort in descending order, based on result
    
    key_list = list(options.keys())     # list keys to access them 
    val_list = list(options.values())   # list values to access them 
    position = val_list.index(results[0])   # find matching value in dictionary 
    sentiment = key_list[position]      # retrieve key value 

    # create and save Sentiment object 

    # get Sentiment object connected to this Article by ID
    sentiment_id = article.sentimentScore.id
    # retrieve the specific Sentiment instance
    temp_sentiment = Sentiment.objects.get(id = sentiment_id)

    # update each field with correct info
    temp_sentiment.mixed = mixed
    temp_sentiment.positive = positive
    temp_sentiment.neutral = neutral
    temp_sentiment.negative = negative
    temp_sentiment.sentiment = sentiment
    temp_sentiment.save(update_fields=['mixed', 'positive', 'negative', 'neutral', 'sentiment'])


    return 'Success - Long Desc Sentiment'



def getSentimentAnalysisSingleURL():
    temp_url = "https://www.reuters.com/world/asia-pacific/us-top-diplomat-blinken-court-southeast-asia-virtual-meetings-next-week-2021-07-31/"
    LANG = "en"
    # get all articles with empty SentimentScore
    x = Article.objects.get(url = temp_url)

    # process each article to get sentiment and save it 
    desc = x.fullDesc        # retrieve full description 
    data = detectSentiment(desc, LANG)  # retrieve AWS results 
    # data = response.json()      

    if data["ResponseMetadata"]["HTTPStatusCode"] != 200:       # make sure results are OK
        return HttpResponse("Failed")
    else:                                   # create model with info from json 

        # get Sentiment object connected to this Article by ID
        sentiment_id = x.sentimentScore.id
        # retrieve the specific Sentiment instance
        temp_sentiment = Sentiment.objects.get(id = sentiment_id)
        # update each field with correct info
        temp_sentiment.mixed = data["SentimentScore"]["Mixed"],
        temp_sentiment.positive = data["SentimentScore"]["Positive"],
        temp_sentiment.neutral = data["SentimentScore"]["Neutral"],
        temp_sentiment.negative = data["SentimentScore"]["Negative"],
        temp_sentiment.sentiment = data["Sentiment"]
        temp_sentiment.save(update_fields=['mixed', 'positive', 'negative', 'neutral', 'sentiment'])

    return HttpResponse("Sentiment Saved")