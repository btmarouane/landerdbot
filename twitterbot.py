import tweepy
import telepot
import configparser
import time
import os
import re

from dotenv import load_dotenv

load_dotenv()
# Read Twitter API keys and access tokens from a properties file
TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# Read Telegram API key and chat id from a properties file
TELEGRAM_API_KEY = os.environ['TELEGRAM_API_KEY']

# Read the properties file
config = configparser.ConfigParser()
config.read("twitterbot.properties")

# Extract the variables from the properties file
TELEGRAM_CHAT_ID = config["DEFAULT"]["TELEGRAM_CHAT_ID"]
KEYWORDS = config["DEFAULT"]["KEYWORD"]
KEYWORDS = KEYWORDS.split(',')
KEYWORDS = [KEYWORD.strip() for KEYWORD in KEYWORDS if len(KEYWORD) > 0]

print(KEYWORDS)
quit()
# Authenticate with Twitter API
auth = tweepy.OAuth1UserHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, TWITTER_ACCESS_TOKEN,
                                TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# Initialize Telegram bot
bot = telepot.Bot(TELEGRAM_API_KEY)

# Read the list of Twitter users to monitor from a file
with open('users.txt', 'r') as f:
    users = f.read().splitlines()

# Set up a dictionary to store the most recent tweet ID for each user
last_tweet_ids = {user: set() for user in users}

while True:
    # Check for new tweets from the users in the list
    for user in users:
        try:
            likes = api.get_favorites(screen_name=user, count=10, tweet_mode="extended")
            current_ids_set = set()
            new_ids_set = set()

            for like in likes:
                current_ids_set.add(like.id)
            for idd in current_ids_set:
                if idd not in last_tweet_ids[user]:
                    new_ids_set.add(idd)

            last_tweet_ids[user] = current_ids_set

            # Iterate through the timeline and check for tweets that contain the keyword
            for like in likes:
                if like.id in new_ids_set:
                    if like.in_reply_to_status_id:
                        continue
                    else:
                        tweet_screen_name = like.user.screen_name
                        tweet_text = like.full_text
                        tweet_preview_url = f"https://twitter.com/twitter/statuses/{like.id}"

                        found_keywords = set()
                        for KEY in KEYWORDS:
                            if re.search(KEY, tweet_text, re.IGNORECASE):
                                found_keywords.add(KEY)

                        if len(found_keywords) > 0:
                            message = f"{user} liked a tweet containing Keywords : {', '.join(found_keywords)}. Url : {tweet_preview_url}"
                            bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=message)
            time.sleep(13)
        except Exception as e:
            print(f"'{user}' failed with error '{e}'")
