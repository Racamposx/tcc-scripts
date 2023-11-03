import os
from dotenv import load_dotenv
import praw
import json
import time
from datetime import datetime

load_dotenv()
start_time = time.time()

reddit = praw.Reddit(client_id=os.getenv("CLIENT_ID"),
                     client_secret=os.getenv("CLIENT_SECRET"),
                     user_agent=os.getenv("USER_AGENT"))

subreddit = reddit.subreddit('DotA2')
dados_posts = []
post_count = 0

def convert_comment_to_dict(comment):
    replies = [convert_comment_to_dict(reply) for reply in comment.replies if isinstance(reply, praw.models.Comment)]
    return {
        "commentId": comment.id,
        "post_id": comment.link_id,
        "parent_id": comment.parent_id,
        "commented_at_timestamp": comment.created_utc,
        "commented_at": datetime.utcfromtimestamp(comment.created_utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "comment": comment.body,
        "vote_score": comment.score,
        "replies": replies
    }

for submission in subreddit.hot(limit=None):
    post_data = {
        "title": submission.title,
        "post_id": submission.id,
        "url": f"https://www.reddit.com{submission.permalink}",
        "created_at_timestamp": submission.created_utc,
        "created_at": datetime.utcfromtimestamp(submission.created_utc).strftime('%Y-%m-%d %H:%M:%S UTC'),
        "vote_score": submission.score,
        "num_comments": submission.num_comments,
        "comments": []
    }

    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        if isinstance(comment, praw.models.Comment):
            comentario_data = convert_comment_to_dict(comment)
            post_data["comments"].append(comentario_data)

    dados_posts.append(post_data)
    post_count += 1


date_creation = datetime.now().strftime("%Y-%m-%d")
with open(f"hotPosts_{date_creation}.json", 'w', encoding='utf-8') as json_file:
    json.dump(dados_posts, json_file, ensure_ascii=False, indent=2)

end_time = time.time()
execution_time = end_time - start_time

print(f"Tempo de execução: {execution_time} segundos")
print(f"total de posts: {post_count}")