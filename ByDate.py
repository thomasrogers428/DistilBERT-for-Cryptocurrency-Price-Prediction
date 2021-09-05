#=========================================================================
# Dartmouth College, LING48, Spring 2021
# Thomas Rogers (Thomas.W.Rogers.23@dartmouth.edu) and Claire McKenna (Claire.L.McKenna.23@dartmouth.edu)
# Final Project: PSAW webscraper for testing data
#
# Based on code from off of PSAW documentation from # code from https://github.com/dmarx/psaw
#
#
# Summary: This program was created to scrape reddit using PSAW in order to get our tested data. It takes data from
# the dates March 1st - May 31st. It accesses two subreddits, bitcoin and ethereum and writes the results to a
# separate file for each subreddit. The posts from each day are separated by the string: "END DAY" so that later
# programs can easily differentiate when posts belong to which day
#
# Inputs: Reddit subreddits: r/bitcoin and r/ethereum
# Output: BTC_posts_1.txt: r/bitcoin post text, with days divided
# by "END DAY", ETH_posts.txt r/ethereum post text, with days divided by "END DAY"
# =========================================================================
import datetime as dt
from psaw import PushshiftAPI

psaw = PushshiftAPI()
all_posts_BTC = []
for j in range(3,6):
    # find days in month
    if j == 3:
        d_range = 31
    elif j == 4:
        d_range = 30
    elif j == 5:
        d_range = 31
    else:
        d_range = 0
    for i in range(d_range):
        # create post list for day
        posts = []
        if i != d_range-1:
            # set start and end time for during month
            start = int(dt.datetime(2021, j, i + 1).timestamp())
            end = int(dt.datetime(2021, j, i + 2).timestamp())
        else:
            # set start and end times for last day of month
            start = int(dt.datetime(2021, j, i + 1).timestamp())
            end = int(dt.datetime(2021, j + 1, 1).timestamp())
        # code from https://github.com/dmarx/psaw
        daily_posts_subs = list(psaw.search_submissions(after=start,
                                                        before=end,
                                                        subreddit='bitcoin',
                                                        limit=300))
        for post in daily_posts_subs:
            posts.append(post.title)
        all_posts_BTC.append(posts)

# repeat process for ETh
all_posts_ETH = []
for j in range(3,6):
    print("j", j)
    if j == 3:
        d_range = 31
    elif j == 4:
        d_range = 30
    elif j == 5:
        d_range = 31
    else:
        d_range = 0
    for i in range(d_range):
        posts = []
        if i != d_range - 1:
            print(i)
            start = int(dt.datetime(2021, j, i + 1).timestamp())
            end = int(dt.datetime(2021, j, i + 2).timestamp())
        else:
            print('else')
            start = int(dt.datetime(2021, j, i + 1).timestamp())
            end = int(dt.datetime(2021, j + 1, 1).timestamp())
        # code from https://github.com/dmarx/psaw
        daily_posts_subs = list(psaw.search_submissions(after=start,
                                                        before=end,
                                                        subreddit='ethereum',
                                                        limit=300))
        for post in daily_posts_subs:
            posts.append(post.title)
        all_posts_ETH.append(posts)

    # create all posts to new text documents
    posttxtBTC = open('BTC_posts_1.txt', 'w')
    for postlist in all_posts_BTC:
        for post in postlist:
            posttxtBTC.write(post + '\n')
        posttxtBTC.write("END DAY" + '\n')

    posttxtETH = open('ETH_posts_1.txt', 'w')
    for postlist in all_posts_ETH:
        for post in postlist:
            posttxtETH.write(post + '\n')
        posttxtETH.write("END DAY  "+ '\n')

