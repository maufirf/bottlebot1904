import facebook
import tweepy
from bottle import *
import json
import os
#from time import time_ns

print('imports finished')

ENV = None
if os.path.exists('auth.json'):
    ENV_FILE = open('auth.json')
    ENV = json.load(ENV_FILE)
    ENV_FILE.close()
else:
    ENV = {
        "FB_ACC_TOKEN":os.environ.get('FB_ACC_TOKEN'),
        "FB_ACC_TOKEN_PAINTMIN":os.environ.get('FB_ACC_TOKEN_PAINTMIN'),
        "TWITTER_CONSUMER_KEY":os.environ.get('TWITTER_CONSUMER_KEY'),
        "TWITTER_CONSUMER_SECRET":os.environ.get('TWITTER_CONSUMER_SECRET'),
        "TWITTER_ACC_TOKEN":os.environ.get('TWITTER_ACC_TOKEN'),
        "TWITTER_ACC_TOKEN_SECRET":os.environ.get('TWITTER_ACC_TOKEN_SECRET'),
    }
FB_PAGE_ID = 111768550255895

db_dir, dump_dir, out_dir, img_dir, db_specifics = define_path_vars()
print('path vars set')
bottles = init_bottles_from_catalogue()
print('bottles initialized')
caps, mids, bottoms = part_classify(bottles)
print('parts initalized')

finbot = super_random_bottle()
print('bottle generated')
impath = f'out.png'
fit_square(finbot[0][0]).save(impath)
print('bottle image saved')

message = get_fusion_name(finbot[1])
comment_message = get_ingredients_as_str(finbot[1])
print(message,comment_message,sep='\n')

print('INITIALIZING SOCIAL MEDIA OBJECTS')
graph = facebook.GraphAPI(ENV["FB_ACC_TOKEN_PAINTMIN"])
print('Facebook Graph API object initialized')
auth = tweepy.OAuthHandler(ENV["TWITTER_CONSUMER_KEY"], ENV["TWITTER_CONSUMER_SECRET"])
auth.set_access_token(ENV["TWITTER_ACC_TOKEN"], ENV["TWITTER_ACC_TOKEN_SECRET"])
api = tweepy.API(auth)
print('Twitter API object initialized')

fb_post = graph.put_photo(image=open(impath, 'rb'), message=message)
post_id = fb_post['post_id']
print(post_id)

fb_comment = graph.put_comment(object_id=post_id, message=comment_message)
print(fb_comment['id'])

posted_tweet = api.update_with_media(impath,message)
print(posted_tweet.id)

posted_reply = api.update_status(comment_message,in_reply_to_status_id = posted_tweet.id)
print(posted_reply.id)