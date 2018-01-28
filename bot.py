import praw
from auth import auth as login
import time

def userFilter(string):
    return string.startswith("/u/")

reddit = praw.Reddit(client_id = login["client_id"],
                     client_secret = login["client_secret"],
                     user_agent = login["user_agent"]);

verifyThreadID = "7rxv0z"

verified = list()
escrow = list()
mods = list()
scam = list()

mods = reddit.subreddit("GarlicMarket").moderator()

verifyThread = reddit.submission(id=verifyThreadID);
verifyThread.comments.replace_more(limit=None)
for tlc in verifyThread.comments:
    if (tlc == None) or (tlc.author == None): # Strip Deleted Comments
        continue
    haveVerified = 0
    requestedVerify = [i[3:].lower().split("\n")[0] for i in tlc.body.split(" ") if userFilter(i)]
    tlc.replies.replace_more(limit=None)
    for reply in tlc.replies:
        if (reply == None) or (reply.author == None): # Strip Deleted Comments
            continue
        while reply.author.name.lower() in requestedVerify:
            haveVerified += 1;
            requestedVerify.remove(reply.author.name.lower())
    print(tlc.author.name + "(" + str(tlc) + ") is lacking verification from " + str(requestedVerify))
    verified.append((tlc.author, haveVerified))

print([i for i in verified if (i[1] > 0)])

USL = reddit.subreddit("UniversalScammerList").wiki['banlist']
scam.extend([i[3:].lower().split("\n")[0] for i in USL.content_md.split(" ") if userFilter(i)])

print(scam)
