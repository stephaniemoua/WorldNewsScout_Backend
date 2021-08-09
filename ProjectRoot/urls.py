"""ProjectRoot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from ProjectAPI import views
from ProjectAPI.views import main

from rest_framework import routers 
router = routers.DefaultRouter()
router.register(r'countries', views.CountryViewSet)
router.register(r'sources', views.SourceViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'articles', views.ArticleViewSet)
router.register(r'spots', views.SpotInstanceViewSet)
# router.register(r'sentiments', views.SentimentViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('getNews/', views.main),
    path('getNews/<str:search>/', views.main),
    path('', include(router.urls)),
]
