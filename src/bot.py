#!/usr/bin/python3.5

import tweepy
import json
import subprocess
import datetime

print("#### " + str(datetime.datetime.now()) +" ####")

#files
ck = open("untracked/secure/consumer_key","r")
cs = open("untracked/secure/consumer_secret","r")
at = open("untracked/secure/access_token","r")
ats= open("untracked/secure/access_token_secret","r")

consumer_key = ck.read().strip()
consumer_secret = cs.read().strip()
access_token = at.read().strip()
access_token_secret = ats.read().strip()

ck.close()
cs.close()
at.close()
ats.close()

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

fID = open("persist/lastID","r")

lastID = int(fID.read().strip())
fID.close()
searchQuery = "@NflTheme"
sfilter = '-filter:retweets'
s = searchQuery + sfilter


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)
        tweet = status
        tweetID = tweet.id
        
        username = tweet.user.screen_name

        inReply = tweet.in_reply_to_status_id
        if( inReply):
            print("reply")
            inReplyTweet = api.get_status(inReply)
            topName = inReplyTweet.user.screen_name
            stweet = json.dumps(inReplyTweet._json, indent = 4)
            jtweet = json.loads(json.dumps(inReplyTweet._json))
            try:
                exURL = jtweet["extended_entities"]["media"][0]["expanded_url"]
            except:
                exURL = "NULL"
            
            isVid = "video" in exURL
            print("Contains video: "+ str(isVid))
            
            if isVid :
                print(".src/dl_and_alter.sh "+exURL)
                subprocess.call(["./src/dl_and_alter.sh", exURL])
                upload_result = api.upload_chunked('untracked/artifacts/out.mp4')
                
                subprocess.call(["sleep","10"])
                #The api needs to upload the video before the status can be posted
                print("updating status")
                try:
                    api.update_status(status="@"+username+" @"+topName+" Are u ready for some football?",in_reply_to_status_id=tweetID, media_ids=[upload_result.media_id_string])
                except tweepy.error.TweepError as e:
                    print(e.response.text)
                    api.update_status(status="@"+username+" @"+topName+"My code broke. Oops",in_reply_to_status_id=tweetID)
                    
                print("cleaning up...")
                subprocess.call(["./src/clean.sh"])
        

myStreamListener = MyStreamListener()

myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=['@NflTheme'])






'''
for tweet in tweepy.Cursor(api.search, s, since_id=lastID, include_entities=True, tweet_mode='extended').items():
    tweetID = tweet.id
    if( tweetID > lastID): lastID = tweetID
    
    username = tweet.user.screen_name

    inReply = tweet.in_reply_to_status_id
    if( inReply):
        print("reply")
        inReplyTweet = api.get_status(inReply)
        topName = inReplyTweet.user.screen_name
        stweet = json.dumps(inReplyTweet._json, indent = 4)
        jtweet = json.loads(json.dumps(inReplyTweet._json))
        try:
            exURL = jtweet["extended_entities"]["media"][0]["expanded_url"]
        except:
            exURL = "NULL"
        
        isVid = "video" in exURL
        print("Contains video: "+ str(isVid))
        
        if isVid :
            subprocess.call(["./src/dl_and_alter.sh", exURL])
            upload_result = api.upload_chunked('untracked/artifacts/out.mp4')
            subprocess.call(["sleep","10"])
            #The api needs to upload the video before the status can be posted
            api.update_status(status="@"+username+" @"+topName+" Are u ready for some football?",in_reply_to_status_id=tweetID, media_ids=[upload_result.media_id_string])
            subprocess.call(["./src/clean.sh"])
    print()

fID = open("persist/lastID","w")
fID.write(str(lastID))
'''