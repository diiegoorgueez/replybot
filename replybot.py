import tweepy
import time
import sys

def get_tweet_id(screen_name):

    try:
        with open("lasttweet.txt", "r") as f:
            lastid = f.read()
    except:
        latesttweet = api.user_timeline(screen_name=screen_name,exclude_replies=True,include_rts=False,count=1)
        return latesttweet[0].id


    latesttweets = api.user_timeline(screen_name=screen_name,exclude_replies=True,include_rts=False,since_id=lastid)

    tweetids = []
    i = 0

    while i < len(latesttweets):
        twid = latesttweets[i].id
        tweetids.append(twid)
        i += 1
    
    if len(tweetids) == 0:
        return 1

    return tweetids

def tweet(twids,message, screen_name, twusername):
    if (isinstance(twids,int)) == False:
        for twid in twids:
            twid = str(twid)
            try:
                tweet = api.update_status(f"@{screen_name} {message}",in_reply_to_status_id=twid)
            except:
                print("There has been an error while trying to reply to the tweet https://twitter.com/" + screen_name + "/status/" + twid)
                sys.exit(2)

            with open("lasttweet.txt", "w") as f:
                f.write(twid)
        
            statusid = tweet.id_str

            print("Tweet sent -> https://twitter.com/" + twusername + "/status/" + statusid)
            time.sleep(5)
    else:
        twids = str(twids)
        try:
            tweet = api.update_status(f"@{screen_name} {message}",in_reply_to_status_id=twids)
        except:
            print("There has been an error while trying to reply to the tweet https://twitter.com/" + screen_name + "/status/" + twids)
            sys.exit(2)

        with open("lasttweet.txt", "w") as f:
            f.write(twids)
            
        statusid = tweet.id_str

        print("Tweet sent -> https://twitter.com/" + twusername + "/status/" + statusid)
        time.sleep(5)

if __name__ == "__main__":

    consumer_key = "PEpZFwjI9qO4Rx40rZZkZtbSV"
    consumer_secret = "peC3H5kkaG2859wLFu1YmG0RXiRyU3EtTt0Q7ulsqdli6eAffv"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, "oob")

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print('Error! Failed to get request token.')

    print("Login with Twitter: %s" % (redirect_url))

    verifier = input("Enter PIN: ")

    try:
        auth.get_access_token(verifier)
    except:
        print("You have entered an invalid PIN")


    api = tweepy.API(auth)

    user = api.verify_credentials()
    twusername = user.screen_name
    print("\nUser %s has logged in successfully.\n" % twusername)

    screen_name = input("What's the username of the target? ")
    message = input("Message to send: ")

    # try:
    twids = get_tweet_id(screen_name)
    tweet(twids,message,screen_name,twusername)
    # except:
    #     print("The user %s hasn't posted new tweets since the last one, specified in the file lasttweet.txt" % screen_name)

    while True:
        time.sleep(300)

        twids = get_tweet_id(screen_name)

        if twids == 1:
            print("The user %s hasn't posted new tweets since the last one, specified in the file lasttweet.txt" % screen_name)
            continue

        tweet(twids,message,screen_name,twusername)


    
