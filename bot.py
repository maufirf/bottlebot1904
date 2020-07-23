import facebook
import tweepy
from bottle import *
import json
import os
from scene import super_random_scene
import requests
from captionstory import get_caption
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
impath = (f'{db_dir}/out.png', f'{db_dir}/out_base.png')
fit_square(finbot[0][0]).save(impath[1])
scene, fusion_name, ingredients, scene_name = super_random_scene((finbot[0][0],finbot[1]))
print('scene generated')
scene.save(impath[0])
print('bottle image saved')

#print('fetching data from api.namefake.com')
#namefake_response = requests.get('https://api.namefake.com/')
#print('fetched, extracting name')
#namefake_dict = json.loads(namefake_response.content)
#namefake_maiden = namefake_dict['maiden_name']
#print(f'extracted name: {namefake_maiden}')

bottle_vol, vol_unit = get_random_volume(finbot[0][0])
#message = '[EXPERIMENT POST - UNSTABLE]\n'+fusion_name+'\nVolume: '+str(bottle_vol)+' '+vol_units[vol_unit]+'s\n\nNote: https://web.facebook.com/bottlebot1904/posts/288772702555478'
#message = f'[EXPERIMENT POST - UNSTABLE]\n{get_caption(namefake_maiden,fusion_name)}\n\nVolume: {str(bottle_vol)}\n\nNote: https://web.facebook.com/bottlebot1904/posts/288772702555478'
#message = f'[EXPERIMENT POST - UNSTABLE]\n{get_caption(fusion_name)}\n\nVolume: {str(bottle_vol)} {vol_units[vol_unit]}s\n\nNote: https://web.facebook.com/bottlebot1904/posts/288772702555478'
message = f'{get_caption(fusion_name)}\n\nVolume: {str(bottle_vol)} {vol_units[vol_unit]}s'
comment_message = ingredients+f'\nBackground: {scene_name}'
print(message,scene_name,comment_message,sep='\n')

print('INITIALIZING SOCIAL MEDIA OBJECTS')
graph = facebook.GraphAPI(ENV["FB_ACC_TOKEN_PAINTMIN"])
print('Facebook Graph API object initialized')
auth = tweepy.OAuthHandler(ENV["TWITTER_CONSUMER_KEY"], ENV["TWITTER_CONSUMER_SECRET"])
auth.set_access_token(ENV["TWITTER_ACC_TOKEN"], ENV["TWITTER_ACC_TOKEN_SECRET"])
api = tweepy.API(auth)
print('Twitter API object initialized')

fb_post = graph.put_photo(image=open(impath[0], 'rb'), message=message)
post_id = fb_post['post_id']
print(post_id)

#fb_comment = graph.put_comment(object_id=post_id, message=comment_message)
#fb_comment = graph.put_object(parent_object=post_id,connection_name='comments',source=('out_base.png',open(impath[1],'rb'),'image/png'),message=comment_message)
fb_comment = graph.put_photo(image=open(impath[1], 'rb'), album_path=f'{post_id}/comments',message=comment_message)
print(fb_comment['id'])

posted_tweet = api.update_with_media(impath[0],message)
print(posted_tweet.id)

posted_reply = api.update_with_media(impath[1],comment_message,in_reply_to_status_id = posted_tweet.id)
print(posted_reply.id)