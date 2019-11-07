# Bottlebot1904
A [Facebook](https://fb.me/bottlebot1904) & [Twitter](https://twitter.com/bottlebot1904) bot that posts an image of a bottle made of other random bottles every hour.

----------------------
![Header image](https://pbs.twimg.com/profile_banners/1188104088832970752/1572803291/1500x500)

**Bottlebot1904** was initally a literal shower thought of KRSmin\* on the end of the day of October 31st, 2019. It was first born in a computer on the KRSmin's university computer lab, and then nutured to his desktop computer. Despite being published on November 3, 2019, the bot is already aired since the beginning of the month. WIthin the first 24 hours of publishing, the Facebook page gains 200 likes, and the Twitter account gains 6 followers (thank you!).

<sub>\*) KRSmin is my alias as a bot admin. the KRS on KRSmin came from my first ever made Discord bot, <a href="https://github.com/parampaa2/krsbot5000">KRSbot500</a>, a bot that posts a random student's semester university study plan card on demand.</sub>


## Deployment
There are some Python dependencies you have to resolve. It is listed on `requirements.txt`, but I'll just rewrite them all here:

- [tweepy](https://www.tweepy.org/) ⩾ 3.8.0 | To post to Twitter
- [facebook_sdk](https://facebook-sdk.readthedocs.io/en/latest/) ⩾ 3.1.0 | To post to Facebook
- [numpy](https://numpy.org/) ⩾ 1.16.2 | Image editing
- [Pillow](https://pillow.readthedocs.io/en/stable/) ⩾ 6.2.1 | Image processing

I am originally using Anaconda3 2019.x on ElementaryOS (Ubuntu distro), which already include the last two and pip-ready.

Also, there's some environment variable you have to set, or you can put these to `auth.json` instead:

- `FB_ACC_TOKEN`, the permanent Facebook **page** access token you obtain by yourself. Optional.
- `FB_ACC_TOKEN_PAINTMIN`, the permanent Facebook **page** access token you obtain from [paintmin's access token tool](https://http://maxbots.ddns.net/token/).
- `TWITTER_CONSUMER_KEY`, the consumer key of your Twitter **app**.
- `TWITTER_CONSUMER_SECRET`, the consumer secret of your Twitter **app**.
- `TWITTER_ACC_TOKEN`, the access token of your Twitter **bot account**.
- `TWITTER_ACC_TOKEN_SECRET`, the access token secret of your Twitter **bot account**.

After everything is set up, you'll just need to run the bot to post **once**, simultaneously to both accounts by simply running the `bot.py`.

## Known bugs
- The image is sometimes at a (quote-unquote) _4kUHD_. The image baked always follow the topmost bottle component size as the anchor. If the topmost component is small, then there is a probability where even the rest of the component is having a high resolution quality would still be rendered pixelated due to the anchor's small size.
- On Facebook, if your main account gets zucced in any sense that forces you to change the password, all of your tokens will expire and you have to renew it

## Acknowledgement
Thank you very much for the support during the first launch. Special shoutout to [Semolini](https://github.com/Boidushya) for tutoring me in the [Bot Appreciation Society Discord server](https://discord.gg/kk6khdj). To all of [Bot Appreciation Society](https://www.facebook.com/groups/botappreciationsociety/) folks who have reacc'd my posts and gave me ideas about what to do. Also to [Michael Reeves](https://www.youtube.com/channel/UCtHaxi4GTYDpJgMSGy7AeSw) that encouraged me to make Twitter bots by his [video making a bot to order 100 random things from Amazon](https://www.youtube.com/watch?v=hBP-NzOadL0&t=634s).
