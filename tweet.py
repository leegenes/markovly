import tweepy, spotify, os
from markovly import Markovly

KEY = os.environ['TWITTER_CONSUMER_KEY']
SECRET = os.environ['TWITTER_CONSUMER_SECRET']
ACC_KEY = os.environ['TWITTER_ACCESS_TOKEN']
ACC_SECRET = os.environ['TWITTER_ACCESS_SECRET']

def get_auth():
    try:
        a = tweepy.OAuthHandler(KEY, SECRET)
        a.set_access_token(ACC_KEY, ACC_SECRET)
        return a
    except:
        print("Permission denied")

def post_update(api, text):
    api.update_status(text)

def tweet():
    lyrics = spotify.gather_lyrics()
    m = Markovly(text=lyrics, n=7, token_type="char")
    m.tokenize()
    verse = m.generate_verse()
    a = get_auth()
    api = tweepy.API(a)
    post_update(api, verse)

if __name__ == "__main__":
    tweet()
