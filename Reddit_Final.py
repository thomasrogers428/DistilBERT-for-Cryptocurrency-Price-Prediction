# =========================================================================
# Dartmouth College, LING48, Spring 2021
# Thomas Rogers (Thomas.W.Rogers.23@dartmouth.edu) and Claire McKenna (Claire.L.McKenna.23@dartmouth.edu)
# Final Project: PSAW webscraper for testing data
#
# Based on code from off of PRAW documentation code from
# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html
#
#
# Summary: This program was created to scrape reddit using PRAW to get the reddit post instances which are used to
# get the titles and time created from r/bitcoin and r/ethereum. The time created of the posts are checked and if
# they fall within the appropriate time window, they are written to the output text files to be labeled
#
# Inputs: Reddit subreddits: r/bitcoin and r/ethereum
# Output: BTC_train.txt and ETH_train.txt: both are plain text
# files with a reddit post title from the respective subreddit on each line.
# =========================================================================
import praw

# https://praw.readthedocs.io/en/latest/getting_started/quick_start.html
# store reddit information
client_id = "kz2khDOTH8OT7Q"
client_secret = "MOa9PcWMNJNWiUvmSt-ssIGEAV9e4w"
user_agent = "CryptoData"
username = "tr428"
password = "CS72LING48"

# initiate reddit instance
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent,
    username=username,
    password=password,
)

# access subreddits
BTC = reddit.subreddit("bitcoin")
ETH = reddit.subreddit("ethereum")

# get reddit posts and make iterable
BTC_LG = BTC.new(limit=20000).__iter__()
ETH_LG = ETH.new(limit=20000).__iter__()

#creates lists for reddit posts
BTC_posts = []
ETH_posts = []

# May 16 2021: 1621137600
# May 23 2021: 	1621742400

# grab reddit posts if between May 16th and May 23rd
for post in BTC_LG:
    if 1621137600 < post.created < 1621742400:
        BTC_posts.append(post)
for post in ETH_LG:
    if 1621137600 < post.created < 1621742400:
        ETH_posts.append(post)

print("BTC Posts", len(BTC_posts))
print("ETH Posts", len(ETH_posts))

# citation: https://www.kite.com/python/answers/how-to-write-a-list-to-a-file-in-python
# write posts to text files
BTC_text = open("BTC_train.txt", "w")
for post in BTC_posts:
    BTC_text.write(post.title + "\n")
BTC_text.close()

ETH_text = open("ETH_train.txt", "w")
for post in ETH_posts:
    ETH_text.write(post.title + "\n")
ETH_text.close()
