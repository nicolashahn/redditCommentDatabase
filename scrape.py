# Aaron Springer
# 3/2/2015
# Scrapes reddit submissions

# To run:
# Needs praw (pip3 install praw)
# python3 scrape.py

import html.parser
import pickle
import praw
SCRAPE_MAX = 4000

r = praw.Reddit(user_agent='cmvScraper Contact EMAIL with concerns/questions')
r.config.store_json_result = True
#user = r.get_redditor('DeltaBot')
#which subreddit to scrape
subreddit = r.get_subreddit('rationality')

# load the ids we have already scraped to avoid redundant scraping
scraped_sub_ids = []
try:
    with open('scrapedSubmissionIDs', 'rb') as f:
        scraped_sub_ids = pickle.load(f)
except FileNotFoundError:
    pass
print('Found scraped submissions: %s' % scraped_sub_ids)
scraped_count = 0
with open('scrapedSubmissions', 'wb') as f:
    try:
        # scrape most popular
        for submission in subreddit.get_top_from_all(limit=4000):
            if scraped_count < SCRAPE_MAX: 
                if submission.id not in scraped_sub_ids:
                    scraped_count += 1
                    scraped_sub_ids.append(submission.id)
                    print('Found new submission: %s' % submission.id)
                    print('Current scrape count: %s/%s' % (scraped_count, SCRAPE_MAX))

                    #flatten the comment tree to avoid pickle recursion limit
                    flat_comments = praw.helpers.flatten_tree(submission.comments, depth_first=True)

                    # now converts the comments from PRAW form to dicts and stuff them back in the subs
                    json_sub = submission.json_dict
                    json_comments = [x.json_dict for x in flat_comments]
                    for comment in json_comments:
                        if comment.get('replies') and comment['replies'] != '':
                            comment['replies'] = [x.name for x in comment['replies']['data']['children']]
                    json_sub['comments'] = json_comments

                    # append the submission(including comments) to the pickled file
                    pickle.dump(json_sub, f)
    except Exception as e:
        print(e)

# dump all the ids so we will know for next scrape
with open('scrapedSubmissionIDs', 'wb') as f:
    pickle.dump(scraped_sub_ids, f)
