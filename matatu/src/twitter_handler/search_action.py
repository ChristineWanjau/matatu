#! /usr/bin/env python

### this file contains implementation for the search feature using the twitter's REST api


import tweepy
from .api_action import TwitterClient
from matatu import models 

def FetchTweets(q):
       ''' internal function for retrieving tweets from database''' 
       list1 = models.TweetObject.objects.filter(query=q)
       if len(list1) < 100:
          list2 = []
          for li in list1:
            list2.append(li.tweet)
          list2.reverse()
          return list2
       else:
         leng = len(list1)
         for i in range(leng-100):
                 list1[i].delete()
         list2 = []
         for li in list1:
            list2.append(li.tweet)
         list2.reverse()
         return list2


def insert():
      ''' accesses the twitter's api to get tweets which match with the query q'''
      api = TwitterClient()
      transport_related_keywords = "KenyanTraffic OR @RoadAlertsKE OR @NTSA_KENYA OR #KenyanTraffic OR road OR #RoadsKE OR @Ma3Route OR #roadalertskenya OR @AccidentAlert_K OR @TAK_Kenya OR sikikasafety OR @KENHAKenya OR @KURAroads OR matatus OR traffic OR transport OR jam OR accident OR road OR highway OR barabara OR drivers"
      public_tweets = api.get_tweets(transport_related_keywords)
      ## putting a filter for tweets in english language only
      for t in public_tweets:
                       # saving latest tweets to database
            p1 =models.TweetObject(date = t['date'],text = t['text'],polarity= t['polarity'],subjectivity = t['subjectivity'],mentions = t['mentions'],hashtags = t['hashtags'],
                                        location = t['location'], route = t['route'],latitude = t['lat'] , longitude = t['lng'], conditions = t['condition'])
            p1.save()
      # most recent tweets from the database will be fetched


# if __name__ == "__main__":
#    insert()



