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

hashtag = "#cancelcusatsemexams"
hashtag2 = "#cusat"
reply_tweets = ["Yes Exactly!!!","KTU exams cancelled.\nNIT exams cancelled.\nIITs cancelled their exams .... Then why can't @CUSAT",
                "I'm really frustrated on conducting present semester exams because how can a student like me whose parents are in quarantine and me who shifted to other home in this pandemic and facing network issues can attend online exams...? How..? I'm really depressed.",
                "@CMOKerala @KeralaGovernor @manoramanews @asianetnewstv @THKerala @IndianExpress \nHave the authorities ever thought of the concerns of students? They have to first prepare for their 3rd sem, then to prepare for the 2nd sem exams and then again bck to 3rd sem",
                "Please cancel CUSAT intermediate sem exams  @KeralaGovernor @CMOKerala @manoramanews @asianetnewstv @THKerala",
"Cusat is again planning to conduct intermediate sem xams during this pandamic.Even IITs and KTU cancelled their exams considering the problems of students but cusat wants to conduct it in between the new semester classesZipper-mouth face @KeralaGovernor @vijayanpinarayi",
"Cusats is also asking for fees of 26k and 40k with fine and superfine. It is acting like a private institute but it still is a govt university. ",
"Notebooks:NO \nProper internet:NO \nStudy materials:NO\nConceptual knowledge:NO\nExams:YES\nAnd you wonder why students commit suicide? ",
"If IITS's and KTU can cancel their sem exams why cant cusat too\n @ShashiTharoor\n@KeralaGovernor\n@asianetnewstv",
"CUSAT is playing with lives of student. First of all they started the new semester and suddenly announced semester exams for the previous semester",
"Dear CUSAT administration, we are not your enemies but students of the college. Why are you treating us like this? Come on, be humble, you also know that our demand is humble. ",
"We are  allready facing lots of  problem coz. Of this pendamic...\nBut cusat wants to conduct old sem exam after starting new sem. It's very hard for students to deal with such situation. Coz students are not even having study materials of previous sem. ",
"CUSAT authorities have released previous sem exam time table out of the blue as an onam gift to their students.this time it is mixed with supply exams too.considering the mental health of students,on going sem,network issues and pandemic,we want cancellation",
"Already this pandemic is putting too much pressure on us students. Conducting even sem exams in the midst of odd sem will only increase our pressure to a frightening level",
"If IITS's and KTU can cancel their sem exams why cant cusat too\n@ShashiTharoor\n@KeralaGovernor\n@asianetnewstv\n@MediaOneTVLive\n@mathrubhuminews\n@manoramanews\n@manoramaonline",
"When covid cases are increasing day by day the ignorance of CUSAT officials is decreasing somehow",
"Not everyone has the same facilities. Some wouldnt have good internet. Gives them a huge  disadvantage . Consider cancelling on the spot evaluations.",
"Currently we are being taught the odd sem portions and now they are demanding us to write the previous even sem examinations within 2 weeks. Its been a long time since we had gone through the Even sem portions.",
"@CMOKerala\n@KeralaGovernor\n@manoramanews\n@asianetnewstv\nEven the KTU and other well known institutes have made the wise decision of promoting students as per UGC guidelines, even then what is forcing CUSAT to conduct exams in the midst of this pandemic.",
"Onam Vacations, no. Study Leave, yes. Immediately after the 'SO CALLED' onam vacations, we have sem exams. Thankyou for the surprise gift university",
"CUSAT is again going to conduct intermediate semester exams during this pandemic but this time it has reached a new level of insane ity \nWe have S3 classes and S2 exams together.Please support our cause.\n@CMOKerala \n@ugc_india\n@KeralaGovernor\n@asianetnewstv",
"The commencement of previous sem exams seems to be taken without considering any points from students part.Student from all classes had raised many concerns unanimously about the viability of conducting previous sem exams in between the ongoing sem.",
"Nobody: The highest pressure on Earth occurs in Siberia.\nCusatian: Hold my beer",
"KTU exams cancelled.\nNIT exams cancelled.\nIITs cancelled their exams .... Then why can't @CUSAT"

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
