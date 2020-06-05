import tweepy
import pandas as p
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from geopy.geocoders import Nominatim
from textblob import TextBlob
import string
import preprocessor as p


# class StdOutListener(StreamListener):
#
#     def on_data(self, data):
#         print(data)
#         return True
#
#     def on_error(self, status):
#         print(status)


class TwitterClient(object):
    

    def __init__(self):
        try:
            API_KEY = '4lmdc41ieBKmnMtVJElU4PDwM'
            API_SECRET_KEY = 'UVhYpjc7W7cVfDczpoQhRV0aL2roY2NhHhgcqpJpTOL9xd3Xe2'
            ACCESS_TOKEN = '1261924787313614848-jKYiBo0kGIuSmbSiaQY6VTVVd4hSkX'
            ACCESS_TOKEN_SECRET = 'kdyf3ligtNf4OgL16XX3nc6vnyarkoMLekCxxb3D7Ebo0'
            self.auth = tweepy.OAuthHandler(API_KEY,API_SECRET_KEY)
            self.auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def get_tweets(self, query):
        start_date = '2020-05-01'

        tweets = []
        gotten_tweets = []
        try:
            for page in tweepy.Cursor(self.api.search, q=query,
                                      count=200, include_rts=False, since=start_date, geocode='-1.28246,36.81994,210km').pages(50):
                for status in page:
                    new_entry = {}
                    status = status._json
                    new_entry['date'] = status['created_at']
                    new_entry['id'] = status['id']

                    ## check whether the tweet is in english or skip to the next tweet
                    if status['lang'] != 'en':
                        continue
                    if status['text'] not in tweets:
                        tweets.append(status['text'])
                        hashtags = ", ".join([hashtag_item['text'] for hashtag_item in status['entities']['hashtags']])
                        new_entry['hashtags'] = hashtags
                        mentions = ", ".join([mention['screen_name'] for mention in status['entities']['user_mentions']])
                        new_entry['mentions'] = mentions


                    # get location of the tweet if possible
                        try:
                           location = status['user']['location']
                        except TypeError:
                           location = ''
                        new_entry['location'] = location

                        try:
                            coordinates = [coord for loc in status['place']['bounding_box']['coordinates'] for coord in loc]
                        except TypeError:
                            coordinates = None
                        new_entry['coordinates'] = coordinates

                        new_entry['text'] = status['text']

                        clean_text = p.clean(status['text'])
                        blob = TextBlob(clean_text)



                    # call clean_tweet method for extra preprocessing
                        filtered_tweet = self.clean_tweet(clean_text)

                    # # pass textBlob method for sentiment calculations

                        Sentiment = blob.sentiment

                    # seperate polarity and subjectivity in to two variables
                        polarity = Sentiment.polarity
                        new_entry['polarity'] = polarity
                        subjectivity = Sentiment.subjectivity
                        new_entry['subjectivity'] = subjectivity
                        new_entry['route'] = self.text_route_classify(filtered_tweet)
                        new_entry['lat'] = self.geocode_lat(new_entry['route'])
                        new_entry['lng'] = self.geocode_lng(new_entry['route'])
                        new_entry['condition'] = self.text_condition_classify(filtered_tweet)
                        gotten_tweets.append(new_entry)
                return gotten_tweets





        except tweepy.Tweepyerror as e:
            print("Error : " + str(e))

    # def get_tweet_sentiment(self, tweet):
    #
    #     analysis = TextBlob(tweet)
    #
    #     if analysis.sentiment.polarity > 0:
    #         return 'positive'
    #     elif analysis.sentiment.polarity == 0:
    #         return 'neutral'
    #     else:
    #         return 'negative'

    def clean_tweet(self,tweet):
        emoticons_happy = set([
            ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
            ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
            '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
            'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
            '<3'
        ])

        # Sad Emoticons
        emoticons_sad = set([
            ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
            ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
            ':c', ':{', '>:\\', ';('
        ])
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)

        emoticons = emoticons_happy.union(emoticons_sad)
        stop_words = set(stopwords.words('english'))


        tweet = re.sub(r':', '', tweet)
        tweet = re.sub(r'‚Ä¶', '', tweet)
        # replace consecutive non-ASCII characters with a space
        tweet = re.sub(r'[^\x00-\x7F]+', ' ', tweet)

        tweet = emoji_pattern.sub(r'', tweet)
        word_tokens = word_tokenize(tweet)

        filtered_tweet = []

        for w in word_tokens:
            if w not in stop_words and w not in emoticons and w not in string.punctuation:
                filtered_tweet.append(w)
        return filtered_tweet

    def text_route_classify(self,tweet):
        route_keywords = ['kibera', 'kangemi','kayole', 'embakasi', 'buruburu', 'mathare', 'rongai', 'huruma','ruai','kangundo',
                          'highrise','roysambu','ngong','githurai','babadogo','outering','msa','eastern','bypass','mombasa','moi','cbd','uhuru','thika','koja','odeon','pangani','juja','ruiru','kenyatta','koinange','utawala','langata']
        for w in tweet:
            if w.lower() in route_keywords:
                if w.lower() == "mombasa":
                    return "mombasa road"
                if w.lower() == "kangundo":
                    return "kangundo road"
                if w.lower() == "langata":
                    return "langata road"
                if w.lower() == "msa":
                    return "mombasa road"
                if w.lower() == "eastern":
                    return "eastern bypass"
                if w.lower() == "bypass":
                    return "eastern bypass"
                if w.lower() == "ngong":
                    return "ngong road"
                if w.lower() == "thika":
                    return "thika road"
                if w.lower() == "uhuru":
                    return "uhuru highway"
                return w.lower()

    def text_condition_classify(self,tweet):
        condition_keywords = ['accident','flooding','slow','jam','stranded','construction','block','roadwork','police','traffic','slippery','hitting','hit','hits','blocking','floods','closure','sidewalks','hazards']

        for w in tweet:
            if w.lower() in condition_keywords:
                if w.lower() == "jam":
                    return "traffic"
                if w.lower() == "slow":
                    return "traffic"
                if w.lower() == "hits":
                    return "accident"
                if w.lower() == "hit":
                    return "accident"
                if w.lower() == "stranded":
                    return "no matatus"
                if w.lower() == "block":
                    return "road block"
                if w.lower() == "closure":
                    return "road closure"
                return w.lower()


    def geocode_lat(self,value):
        geolocator = Nominatim(user_agent= "digital_matatu")
        if value is None:
            return None
        location = geolocator.geocode(value, timeout=20)
        lat = location.latitude
        return lat

    def geocode_lng(self,value):
        if value is  None:
            return None
        geolocator = Nominatim(user_agent= "digital_matatu")
        location = geolocator.geocode(value, timeout= 20)
        lng = location.longitude
        return lng
# if __name__ == "__main__":
#     api = TwitterClient()
#     transport_related_keywords = "KenyanTraffic OR Road Alerts OR NTSA_KENYA OR #KenyanTraffic OR roadOR Ma3Route OR #roadalertskenya OR AccidentAlert_K OR TAK_Kenya OR sikikasafety OR KENHAKenya OR KURAroads OR matatus OR traffic OR transport OR jam OR accident OR road OR highway"
#     tweets =  api.get_tweets(transport_related_keywords)
#     print(tweets)
