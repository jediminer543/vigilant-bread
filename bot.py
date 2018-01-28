import praw
from auth import auth as login

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
verifyThread.comments.replace_more(limit=0)
for tlc in verifyThread.comments:
    haveVerified = 0
    requestedVerify = [i[3:] for i in tlc.body.split(" ") if userFilter(i)]
    tlc.replies.replace_more(limit=0)
    for reply in tlc.replies:
        try:
            if reply.author.name in requestedVerify:
                haveVerified += 1;
                requestedVerify.remove(reply.author.name)
        except Exception as e:
            print(e)
            print(reply)
    verified.append((tlc.author, haveVerified))

print([i for i in verified if (i[1] > 0)])
