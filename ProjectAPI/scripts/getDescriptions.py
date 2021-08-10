#   Scrapes content for ONE article based on news source HTML pattern:
#   - identify source provided 
#   - calls the method that extract the correct HTML pattern 

#   Supported sources:
#   US: Reuters, The Verge, The Hill, TechCrunch, NPR, CNN, Associated Press
#   CA: Financial Post, CBC News 
#   AU: News AU, ABC AU
#   GB: The independent, BBC 


from bs4 import BeautifulSoup
import requests
from ProjectAPI.models import Article


###############################################
# MAIN FUNCTION 
# for each article, scrape full content for analysis
# update article field 'fullDesc' 
def getDescriptions():
    articles_empty = Article.objects.filter(fullDesc = "")
    for article in articles_empty:                                    # for each article, add the content
        desc = getArticleContent(article.get_source_id(), article.url)             # retrieve article content
        
        # if (desc == 'ErrorExtraction'):
        #     # delete articles? 
        #     continue 
            
        # else: 
        article.fullDesc = desc
        article.save(update_fields=['fullDesc'])

    return "Descriptions Saved"

def getArticleContent(sourceId, url):
    # options = { 'independent': extractIndependent(url), 'bbc-news': extractBBC(url), 
    #             'news-com-au': extractNewsAU(url), 'abc-news-au': extractAbcAU(url),
    #             'financial-post': extractFinancialPost(url), 'cbc-news': extractCBCNews(url),
    #             'the-verge': extractTheVerge(url), 'the-hill': extractTheHill(url),
    #             'techcrunch': extractTechCrunch(url), 'politico': extractPolitico(url),
    #             'npr': extractNPR(url), 'cnn': extractCNN(url), 
    #             'associated-press': extractAssociatedPress(url), 'reuters': extractReuters(url)
    # }

    # if sourceId in options:
    #     options[sourceId]()

    ### GB sources ###
    if sourceId == "independent":
        # id = "main"
        return extractIndependent(url)

    if sourceId == "bbc-news":
        return extractBBC(url)
    
    ### AU sources ###
    if sourceId == "news-com-au":
        return extractNewsAU(url)
    
    if sourceId == "abc-news-au":
        return extractAbcAU(url)

    ### CA sources ###
    if sourceId == "financial-post":
        return extractFinancialPost(url)

    if sourceId == "cbc-news":
        return extractCBCNews(url) 

    ### US sources ###
    if sourceId == "the-verge":
        return extractTheVerge(url)

    if sourceId == "the-hill":
        return extractTheHill(url)

    if sourceId == "techcrunch":
        return extractTechCrunch(url)

    if sourceId == "politico":
        return extractPolitico(url)

    if sourceId == "npr":
        return extractNPR(url)

    if sourceId == "cnn":
        return extractCNN(url)

    if sourceId == "associated-press":
        return extractAssociatedPress(url)
     
    if sourceId == "reuters":
        return extractReuters(url)

    else:
        return ("Failed - source not found")
     
###############################################
################# Process GB sources ##################
def extractIndependent(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    
    # find HTML element by class name 
    results = soup.find(id="main")
    try: 
        article_body = results.text

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

def extractBBC(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    
    # find HTML element by class name 
    results = soup.find_all("div", class_= "ssrcss-uf6wea-RichTextComponentWrapper")
    
    try: 
        article_body = ''
        for item in results:
            article_body += item.text
            article_body += "\n"

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

###############################################
################# Process AU sources ##################
def extractNewsAU(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    
    # find HTML element by class name 
    results = soup.find("div", class_="story-content").find_all('p')
    article_body = ''

    try: 
        for item in results:
            # if item.find("div", class_="newsletter-content") is True:
            #     article_body += ""
            # else: 
            article_body += item.text
            article_body += "\n"

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

def extractAbcAU(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    
    # find HTML element by class name 
    results = soup.find("div", class_="ZN39J").find_all('p', class_="_1HzXw")
    article_body = ''

    try:
        for item in results:
            article_body += item.text
            article_body += "\n"
        
        results = soup.find("div", class_="ZN39J").find_all('h2', class_="_2O2Ne")

        for item in results:
            article_body += item.text
            article_body += "\n"

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

# def extractFinancialReviewAU(url):
#     print("hello world")

###############################################
################# Process CA sources ################## 

# paywall / subscription required for full text
# def extractGlobeMail(url):
#     print("hello world")

# prints error message from video not loading 
def extractFinancialPost(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    temp = ''

    try: 
        # article subtitle 
        results = soup.find("p", class_= "article-subtitle") #reuters 
        temp += results.text.strip()

        # article content
        results = soup.find("article", class_="article-content-story").find_all("section", class_= "article-content__content-group")

        for item in results:
            temp += item.text.strip()
            temp += "\n"

        article_body = temp.replace('Article content', '')

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

def extractCBCNews(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    
    # find HTML element by class name 
    results = soup.find("div", class_="story")
    try: 
        article_body = results.text

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

###############################################
################# Process US sources ##################

# paywall / subscription requirement
# def extractWired():
#     print("hello world")

def extractReuters(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    
    # find HTML element by class name 
    results = soup.find("div", class_= "ArticleBody__content___2gQno2") 

    try:
        article_body = results.text.strip()

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

def extractTheVerge(url):
    
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    
    # find HTML element by class name 
    results = soup.find("div", class_= "c-entry-content") 

    try: 
        article_body = results.text.strip()

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

def extractTheHill(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    
    # find HTML element by class name 
    results = soup.find("div", class_="field-item even").find_all('p')
    article_body = ''

    try: 
        for item in results:
            article_body += item.text
            article_body += "\n"

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

def extractTechCrunch(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    
    # find HTML element by class name 
    results = soup.find("div", class_="article-content").find_all('p')
    article_body = ''

    try: 
        for item in results:
            article_body += item.text
            article_body += "\n"

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

def extractPolitico(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    article_body = ''

    results = soup.find_all("div", class_="story-text")

    try: 
        for item in results:
            article_body += item.text.strip()
            article_body += "\n"

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

# prints image information 
def extractNPR(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    article_body = ''

    results = soup.find("div", class_="storytext").find_all('p')

    try: 
        for item in results:
            article_body += item.text.strip()
            article_body += "\n"

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

#l-container
# div class="el__leafmedia"
# zn-body__paragraph 
def extractCNN(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    article_body = ''

    try:
        results = soup.find("div", class_="l-container").find_all('p', class_="zn-body__paragraph")

        for item in results:
            article_body += item.text.strip()
            article_body += "\n"

        results = soup.find("div", class_="l-container").find_all('div', class_="zn-body__paragraph")

        for item in results:
            article_body += item.text.strip()
            article_body += "\n"

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)

def extractAssociatedPress(url):
    page = requests.get(url)  #go to URL
    soup = BeautifulSoup (page.content, "html.parser")  #create beautiful soup object with page.content
    article_body = ''
    temp = ''

    results = soup.find("div", class_="Article")
    try: 
        for item in results:
            # print(item )
            temp += item.text.strip()
            temp += "\n"

        article_body = temp.replace('ADVERTISEMENT', '')

    except:
        article_body = "ErrorExtraction"

    finally: 
        return(article_body)


##############################################
################# TEST CODE ##################
# description = getArticleContent_All(sourceId, url)
# print (description)

# sourceId = "reuters"
# url = "https://www.reuters.com/world/us/us-plans-give-extra-covid-19-shots-at-risk-americans-fauci-2021-08-05/"

# sourceId = "independent"
# url = "https://www.independent.co.uk/sport/olympics/lara-trump-gwen-berry-olympics-b1895222.html"

# sourceId = "the-verge"
# url = "https://www.theverge.com/2021/7/23/22589285/gm-super-cruise-automatic-lane-change-gmc-chevy-silverado"

# sourceId = "bbc-news"
# url = "https://www.bbc.com/news/world-asia-58051481"

# sourceId = "news-com-au"
# url = "https://www.news.com.au/national/queensland/news/intimate-partner-visits-deemed-not-essential-under-qld-lockdown/news-story/acd8890c2508f32e62d72afa68cfb455"

# sourceId = "abc-news-au"
# url = "https://www.abc.net.au/news/2021-08-04/operation-covid-shield-rollout-questions-scott-morrison/100347820"

# sourceId = "financial-post"
# url = "https://financialpost.com/personal-finance/high-net-worth/whos-jim-pattison-empire-builder-and-billionaire-just-dont-call-him-canadas-warren-buffett"

# sourceId = "cbc-news"
# url = "https://www.cbc.ca/news/canada/edmonton/opposition-ndp-calls-for-public-inquiry-into-alberta-s-covid-19-response-1.6128220"

# sourceId = "the-hill"
# url = "https://thehill.com/homenews/administration/566223-cdc-issues-eviction-moratorium-extension-after-democratic-outcry"

# sourceId = "techcrunch"
# url = "https://techcrunch.com/2021/08/03/gig-companies-take-worker-classification-fight-to-massachusetts-through-ballot-initiative/"

# sourceId = "politico"
# url = "https://www.politico.com/news/2021/08/03/cori-bush-eviction-crisis-502313"

# sourceId = "npr"
# url = "https://www.npr.org/2021/08/03/1024345276/the-biden-administration-plans-a-new-eviction-moratorium-after-a-federal-ban-lap"

# sourceId = "cnn"
# url = "https://www.cnn.com/2021/08/04/health/vaccinated-people-return-to-work-wen-wellness/index.html"

# sourceId = "associated-press"
# url = "https://apnews.com/article/business-health-china-coronavirus-pandemic-292b84b26eb41888c579a6460c2647c3"

