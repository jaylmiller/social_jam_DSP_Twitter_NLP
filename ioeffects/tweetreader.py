#Test Code for dealing with python and twitter
from twython import TwythonStreamer
from textblob import TextBlob
import decimal
import django
django.setup()
from settings.models import Twitter

TERMS = "#ioeffects"

#Twitter authentication stuff
APP_KEY = 'eVUo971BGEMWoEkUtILBfZmFI'
APP_SECRET = 'HvWIrgdxp8LRCUT6J2YeNQSJJ0InB8keLi2mAoBIRUNq4s94qE'
OAUTH_TOKEN = '412544630-xhKOQClnvSbZq68qmH6Q1PQpmI5lCmfPS6c841On'
OAUTH_TOKEN_SECRET = 'HvbNOcw2ZYRDdjnbVVroi7IXFeOfDd4D7X50WT8p09mib'


#Callbacks for twython streamer
class FireAssStreamer(TwythonStreamer):
    def on_success(self, data):
        if 'text' in data:
            blob = TextBlob(data['text'].encode('utf-8'))
            bird = Twitter.objects.get(pk=1)
            vibe = blob.sentiment.polarity
            bird.modifier = (decimal.Decimal(.3) * decimal.Decimal(vibe)) + (decimal.Decimal(.7) * bird.modifier) 
            bird.save()
            print "New Tweet"
            print "Polarity: " + str(decimal.Decimal(vibe))
            print data['text'].encode('utf-8')
            print "__________________________"

#create streamer
stream = FireAssStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track=TERMS)
