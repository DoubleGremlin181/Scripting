import praw
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

print "The Headlines for today are:"

r = praw.Reddit(user_agent='Test script')
submissions = r.get_subreddit('worldnews').get_hot(limit=10)
for x in submissions:
    print str(x.title) +"\n"
