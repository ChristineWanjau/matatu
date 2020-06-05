from django.urls import path
from . import views

urlpatterns = [
    path('', views.mapCoordinates,name="map"),
    path('charts/', views.pie_chart, name="charts"),
    path('raw_tweets/',views.raw_tweets, name="raw_tweets"),
    path('positive_tweets/', views.positive_tweets, name="positive_tweets"),
    path('negative_tweets/', views.negative_tweets, name="negative_tweets"),
    path('graph/', views.graph, name="graph"),
    path('construction/', views.heatmap, name="construction"),
    path('reload_tweet/', views.reload_tweets,name="reload_tweet"),
    path('conditions/', views.graph_condition, name="conditions"),
    path('police_sentiment/', views.police_sentiment, name="police_sentiment"),
    path('tweet_table/', views.tweet_table,name = "tweet_table"),
    path('senti/', views.sentiments, name="senti"),
    path('mapping/', views.mapping, name="getmap"),
]   