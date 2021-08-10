# from ..models import Article, Topic 
# from ProjectRoot.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, REGION
# import boto3
# import json
# import requests 
# from django.http import HttpResponse
# from rest_framework.response import Response
# from bs4 import BeautifulSoup
# import time

# #############################
# import numpy as np
# import json
# import glob
# #Gensim
# import gensim
# import gensim.corpora as corpora
# from gensim.utils import simple_preprocess
# from gensim.models import CoherenceModel
# #spacy
# import spacy
# from nltk.corpus import stopwords
# #vis
# # import pyLDAvis
# # import pyLDAvis.gensim
# import warnings
# warnings.filterwarnings("ignore", category=DeprecationWarning)

# stopwords = stopwords.words("english")


# COUNTRY_LIST = ["us", "ca", "gb", "au"]
# PATH_LIST = ["topicFolder_us/", "topicFolder_us", "topicFolder_us", "topicFolder_us"]

# # S3 topic destinations:
# PATH_US = "topicFolder_us/"
# PATH_CA = "topicFolder_ca/"
# PATH_GB = "topicFolder_gb/"
# PATH_AU = "topicFolder_au/"
# PATH_WW = "topicFolder_ww/"

# TM_PATH_US = "tm_results_us/"
# TM_PATH_CA = "tm_results_ca/"
# TM_PATH_GB = "tm_results_gb/"
# TM_PATH_AU = "tm_results_au/"
# TM_PATH_WW = "tm_results_ww/"

# # Default bucket name 
# BUCKET_NAME = 's-m-sum221-wns'

# s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
#                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#                       region_name=REGION)
# comprehend = boto3.client('comprehend', aws_access_key_id=AWS_ACCESS_KEY_ID, 
#                     aws_secret_access_key=AWS_SECRET_ACCESS_KEY, 
#                     region_name=REGION)
    
# # for each country: 
#     # save each article description as a S3 file 
#     # run a topic analysis for the country's folder 
# # retrieve the data to create Topics cards 
# # attach topic cards to country
# # attach topic cards to articles 
# # populate the SpotInstance cards 

# def addTopicModeling():
#     # save each article into country folder on S3
#     # saveToS3('us', PATH_US)
#     # saveToS3('ca', PATH_CA)
#     # saveToS3('gb', PATH_GB)
#     # saveToS3('au', PATH_AU)
#     print(stopwords)
#     #runTopicModeling(PATH_US, TM_PATH_US)
#     # runTopicModeling(PATH_CA)
#     # runTopicModeling(PATH_GB)
#     # runTopicModeling(PATH_AU)

#     return "success"

# # save fullDesc as S3 file: ONE_DOC_PER_FILE
# # name doc with article_id
#  # one bucket per country
# def saveToS3(country, path):
#     articles = Article.objects.filter(source__locale__countryId = country)  # get all articles 
    
#     for article in articles:       # save to S3 
#         data = article.fullDesc     # get the content to save 
#         dest_path = path + str(article.id) +'.txt'
#         response = s3.put_object(Bucket=BUCKET_NAME,Key= dest_path, Body = data)

#     return response 

# # AWS returns up to 25 topics, each with 10 words attached
# def runTopicModeling(pathInput, pathOutput):
#     input_s3_url = "s3://" + BUCKET_NAME +"/"+ pathInput
#     input_doc_format = "ONE_DOC_PER_FILE"
#     output_s3_url = "s3://" + BUCKET_NAME +"/"+ pathOutput
#     number_of_topics = 10

#     input_data_config = {"S3Uri": input_s3_url, "InputFormat": input_doc_format}
#     output_data_config = {"S3Uri": output_s3_url}
#     data_access_role_arn = 'arn:aws:iam::714063285346:role/wns_role'

#     start_topics_detection_job_result = comprehend.start_topics_detection_job(NumberOfTopics=number_of_topics,
#                                                                               InputDataConfig=input_data_config,
#                                                                               OutputDataConfig=output_data_config,
#                                                                               DataAccessRoleArn=data_access_role_arn)
#     job_id = start_topics_detection_job_result['JobId']

#     while True:
#         result = comprehend.describe_topics_detection_job(JobId=job_id)
#         job_status = result["TopicsDetectionJobProperties"]["JobStatus"]

#         if job_status in ['COMPLETED', 'FAILED']:
#             print("job_status: " + job_status)
#             break
#         else:
#             print("job_status: " + job_status)
#             time.sleep(60)

#     return job_id

# def generateCountryTopics(country, destination):   # One country at a time
#     return 0
# # from S3 file, get top 5 topics
# # create 5 topics objects with keyword + list of terms


# def generateArticleTopics():   # one country at a time
#     return 0
# # from S3 file,
# # for each document in bucket
#   # articleID = get name of document 
#   # topicID = get topic ID
#   # add TopicID to articleID