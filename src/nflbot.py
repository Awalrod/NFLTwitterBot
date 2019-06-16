#!/usr/bin/python3.5
import sys
import tweepy
import json
import subprocess
import datetime
import time


#Copied from installer
#TODO centralize these in a config file
BINLOC="/usr/local/bin"
LOGLOC="/var/log"
PERSISTLOC="/etc/nflbot"
SECLOC=PERSISTLOC+"/secure"
TEMPLOC=PERSISTLOC+"/tmp"
PYLIBLOC="/usr/local/lib/python3.5/dist-packages"
DAEMONLOC="/etc/init.d"


print("Iinitial start: "+str(datetime.datetime.now()))

while(True):
    print("#### " + str(datetime.datetime.now()) +" ####")

    #files
    ck = open(SECLOC+"/consumer_key","r")
    cs = open(SECLOC+"/consumer_secret","r")
    at = open(SECLOC+"/access_token","r")
    ats= open(SECLOC+"/access_token_secret","r")

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

    fID = open(PERSISTLOC+"/lastID","r")

    lastID = int(fID.read().strip())
    fID.close()
    searchQuery = "@NflTheme"
    sfilter = '-filter:retweets'
    s = searchQuery + sfilter

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
                subprocess.call(["dl_and_alter.sh", exURL])
                upload_result = api.upload_chunked(TEMPLOC+"/out.mp4")
                subprocess.call(["sleep","10"])
                #The api needs to upload the video before the status can be posted
                api.update_status(status="@"+username+" @"+topName+" Are u ready for some football?",in_reply_to_status_id=tweetID, media_ids=[upload_result.media_id_string])
                subprocess.call(["nflclean.sh"])
        print()

    fID = open(PERSISTLOC+"/lastID","w")
    fID.write(str(lastID))
    fID.close()
    time.sleep(300) # 5 minutes    