import os
import pickle
import tweepy
import datetime

def load_api(file='credentials.pkl'):
    cred = pickle.load(open(file, 'rb'))
    auth = tweepy.OAuthHandler(cred['consumer_key'], cred['consumer_secret'])
    auth.set_access_token(cred['access_token'], cred['access_token_secret'])
    api = tweepy.API(auth)
    
    return api

class StreamListener(tweepy.StreamListener):
    def __init__(self, file, lang, query, tweet_limit=100):
        super(StreamListener, self).__init__()
        self.file = file
        self.lang = '|'.join(lang)
        self.query = '|'.join(query)
        self.tweet_limit = tweet_limit
        self.i = 0
        
    def on_connect(self):
        if not os.path.exists(self.file):
            with open(self.file, 'w') as f:
                f.writelines('time,lang,query,user,text\n')
            
        print(f'---Stream opened ({self.file})---')
        
    def on_status(self, status):
        time = status.created_at - datetime.timedelta(hours=5)
        time = time.strftime("%Y-%m-%d %H:%M:%S")
        text = status.text.replace('"', "'")
        text = f'"{text}"'
        
        with open(self.file, 'a') as f:
            f.writelines(time + ',')
            f.writelines(self.lang + ',')
            f.writelines(self.query + ',')
            f.writelines(status.user.screen_name + ',')
            f.writelines(text)
            f.writelines('\n')
        
        self.i += 1
        if self.i < self.tweet_limit:
            print(f'{self.i}/{self.tweet_limit}', end='\r')
        else:
            print(f'---Got {self.tweet_limit} tweets---')
            return False
        
    def on_error(self, status_code):
        print(f'---Got error: {status_code}---')
        return False

    def on_disconnect(self, notice):
        print('---Stream closed---')
        
        
