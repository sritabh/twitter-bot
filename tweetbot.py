import tweepy
import time
import logging
import random
import os
from os import environ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
# Authenticating to to Twitter
API_KEY = environ["API_KEY"]
API_SKEY = environ["API_SKEY"]
ACC_Token = environ["ACC_Token"]
ACC_Token_Secret = environ["ACC_Token_Secret"]
auth = tweepy.OAuthHandler(API_KEY,API_SKEY)
auth.set_access_token(ACC_Token,ACC_Token_Secret)
api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)
FILE_NAME = 'last_seen_id.txt' #contains time for last tweet

hashtag = "#CusatWantsGeneralPromotion"
hashtag2 = "#cusat"
reply_tweets = ["Yes Exactly!!!","Cutting down a 3 hour exam to 2 hours leaves students at a loss as poor internet connections and unreliable.."
            ,"No study materials, no classes ,intermediate semesters exams should be canceled. Let them conduct Supply mentry exams, bcz students have already attended the classes"
            ,"We dont even have books to study for the exams. We all left our hostels in a hurry. And our university is interested in conducting exams so that they could collect next sem fees and exam fees. #StudentsLivesMatter "
            ,"Cancel the examinations",
            "It is extremely unfair to conduct exams during the Covid19 pandemic.",
            "Iits and nits cancelled the exam and decided to give result on the basis of internal marks and previous year sem exam then why not cusat",
            "degree>>>education ?",
            "Iits and nits cancelled the exam and decided to give result on the basis of internal marks and previous year sem exam then why not cusat",
            "Camera on, video call, asking for live locations. What are you ? My girlfriend ?",
            "Less than 5 days given for external preparation  #cusatexams #speakupforstudents #cusat #ugc",
            "Taking exams after reading ppts in online classes. This is not fair #cusat #speakupforstudents #cancelallexams",
            "Teaching one question is enough for one chapter. Is this a fair move?",
            "Conducting exams after taking 2hr online class to complete 1 week course is not fair",
            "If other exams can cancel the exams why not #CUSAT #Cusatexams",
            "It looks like our opinion doesn't matters",
            "It's not fair to have exams in between the pandemic everyone is suffering either mentally or physically!"
            ]
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return
def retweet_and_like(tweet):
    if not tweet.favorited:
        # Mark it as Liked, since we have not done it yet
        try:
            tweet.favorite()
        except:
            logger.error("Error in liking tweet", exc_info=True)
    if not tweet.retweeted:
        # Retweet, since we have not retweeted it yet
        try:
            tweet.retweet()
        except:
            logger.error("Error on retweet", exc_info=True)
def reply_to_tweets():
    print('Fetching tweet...', flush=True)
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    mentions = api.mentions_timeline(
                        last_seen_id,
                        tweet_mode='extended') #get full tweet with extended
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text, flush=True)
        last_seen_id = mention.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        if hashtag or hashtag2 in mention.full_text.lower():
            retweet_and_like(mention)
            print('found ' +hashtag, flush=True)
            print('Responding tweet', flush=True)
            n = random.randint(0,len(reply_tweets)-1)
            try:
                api.update_status('@' + mention.user.screen_name +
                        ' '+reply_tweets[n]+" "+hashtag, mention.id)
            except:
                logger.error("Error replying to the tweet", exc_info=True)

while True:
    reply_to_tweets()
    time.sleep(15)