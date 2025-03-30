import praw
import random
import json
import re
from datetime import datetime
from gemini_ai import get_gemini_response, get_gemini_subreddits

def analyze_user(username: str) -> list:
    """
    Given a Reddit username, look up the user's public submissions and comments,
    then call get_gemini_subreddits to obtain three likely subreddits of interest.
    Next, gather alternate users from those subreddits and, for each alternate user,
    build their profile string and call get_gemini_response individually to get a compatibility score.
    Finally, order the results and return the top three most compatible users.
    """
    # Initialize the Reddit instance (using application credentials)
    reddit = praw.Reddit(
        client_id="zZGeWFS_82tBIYtg_4FXjw",         # Your actual client_id
        client_secret="2-k9TByNoT8qLWP1HUeHO85pyPWUOQ", # Your actual client_secret
        user_agent="Rinder-Scraper"                     # A descriptive user_agent for your app
    )
    
    # Retrieve the target user's public data
    try:
        user_obj = reddit.redditor(username)
    except Exception as e:
        print(f"Error looking up user {username}: {e}")
        return []
    
    # Scrape the user's recent submissions and comments (limit to 20 each)
    user_submissions = list(user_obj.submissions.new(limit=20))
    user_comments = list(user_obj.comments.new(limit=20))
    
    # Build arrays of submission and comment strings for the target user
    submission_arr = []
    for submission in user_submissions:
        ctime = datetime.utcfromtimestamp(submission.created_utc)
        ftime = ctime.strftime('%Y-%m-%d %H:%M:%S')
        details = (
            f"Title: {submission.title}\n"
            f"URL: {submission.url}\n"
            f"Score: {submission.score}\n"
            f"Created: {ftime}\n"
        )
        if submission.is_self:
            details += f"Selftext: {submission.selftext}\n"
        submission_arr.append(details)
    
    comment_arr = []
    for comment in user_comments:
        ctime = datetime.utcfromtimestamp(comment.created_utc)
        ftime = ctime.strftime('%Y-%m-%d %H:%M:%S')
        details = (
            f"Comment: {comment.body}\n"
            f"Score: {comment.score}\n"
            f"Created: {ftime}\n"
            f"In submission: {comment.submission.title}\n"
        )
        comment_arr.append(details)
    
    # Aggregate the target user's profile into a single string (Profile 1)
    top_submissions = "\n".join(submission_arr)
    top_comments = "\n".join(comment_arr)
    user_data_str = (
        f"Username: {username}\n"
        f"Top 20 Submissions:\n{top_submissions}\n"
        f"Top 20 Comments:\n{top_comments}\n"
    )
    
    # Get likely subreddits for this user via Gemini (assumed to return a dict or list of subreddit names)
    likely_subreddits = get_gemini_subreddits(user_data_str)
    # If likely_subreddits is a dict, take its values; otherwise, assume it's a list.
    if isinstance(likely_subreddits, dict):
        likely_subreddits = list(likely_subreddits.values())
    print(f"Likely subreddits for {username}: {likely_subreddits}")
    
    # Gather alternate users from these subreddits
    alternate_usernames = []
    for subreddit in likely_subreddits:
        try:
            subreddit_obj = reddit.subreddit(subreddit)
            active_names = []
            # Use recent comments to determine active users (up to 10 per subreddit)
            for comment in subreddit_obj.comments(limit=50):
                if comment.author and comment.author.name not in active_names:
                    active_names.append(comment.author.name)
                if len(active_names) >= 5:
                    break
            alternate_usernames.extend(active_names)
        except Exception as e:
            print(f"Error retrieving active users from r/{subreddit}: {e}")
    alternate_usernames = list(dict.fromkeys(alternate_usernames))  # deduplicate
    
    # For each alternate user, build their profile string (top 20 submissions and top 20 comments)
    compatibility_results = []  # Will hold tuples: (alt_username, compatibility_score, full_response)
    for alt_uname in alternate_usernames:
        try:
            alt_user = reddit.redditor(alt_uname)
            alt_submissions = []
            for submission in alt_user.submissions.new(limit=20):
                ctime = datetime.utcfromtimestamp(submission.created_utc)
                ftime = ctime.strftime('%Y-%m-%d %H:%M:%S')
                alt_submissions.append(
                    f"Title: {submission.title}\nURL: {submission.url}\nScore: {submission.score}\nCreated: {ftime}\n"
                )
            alt_comments = []
            for comment in alt_user.comments.new(limit=20):
                ctime = datetime.utcfromtimestamp(comment.created_utc)
                ftime = ctime.strftime('%Y-%m-%d %H:%M:%S')
                alt_comments.append(
                    f"Comment: {comment.body}\nScore: {comment.score}\nCreated: {ftime}\nIn submission: {comment.submission.title}\n"
                )
            top_alt_submissions = "\n".join(alt_submissions)
            top_alt_comments = "\n".join(alt_comments)
            alt_data_str = (
                f"Username: {alt_uname}\n"
                f"Top 20 Submissions:\n{top_alt_submissions}\n"
                f"Top 20 Comments:\n{top_alt_comments}\n"
            )
            
            # Call Gemini for this alternate user
            response_json = get_gemini_response(user_data_str, alt_data_str)
            # Expecting a response that includes "compatibility_score"
            compatibility_score = response_json.get("compatibility_score", 0)
            compatibility_results.append((alt_uname, compatibility_score, response_json))
        except Exception as e:
            print(f"Error processing alternate user {alt_uname}: {e}")
    
    # Order the alternate users from highest to lowest compatibility score
    compatibility_results.sort(key=lambda x: x[1], reverse=True)
    # Return the top three most compatible users
    top_3 = compatibility_results[:3]
    return top_3