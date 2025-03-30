
import google.generativeai as genai
import json
import re

genai.configure(api_key='AIzaSyBlJcdu8CZwJWnCxGj0jZcFGu_cEGo5azU')  # Replace with your actual API key
model = genai.GenerativeModel('gemini-2.0-flash')

def get_gemini_response(profile1_text: str, profile2_text: str) -> dict:
    prompt = f"""
    You are an expert at analyzing text-based social media profiles to evaluate compatibility.

    Analyze the compatibility of these two Reddit profiles thoroughly, considering interests, style of communication, subreddit overlap, personality, and possible compatibility for friendship or romantic relationship.

    Return your answer ONLY in structured JSON as follows:
    {{
        "compatibility_score": int (0-100),
        "relationship_type": "Friendship" / "Romantic" / "Low compatibility",
        "common_interests": ["list", "of", "common", "interests"],
        "compatibility_summary": "a brief insightful paragraph explaining compatibility reasons"
    }}

    Profile 1:
    {profile1_text[:4000]}

    Profile 2:
    {profile2_text[:4000]}
    """
    
    try:
        response = model.generate_content(prompt)
        #print(response)
        #print(response.candidates[0].content)

        # Assume we take the first candidate's text
        raw_text = response.candidates[0].content.parts[0].text

        # Use a regex to extract the JSON inside triple backticks
        
        match = re.search(r"json\s*(\{.*\})\s*", raw_text, re.DOTALL)
        if match:
            json_text = match.group(1)
        else:
            # If the code fences aren't found, fallback to the raw text stripped.
            json_text = raw_text.strip()
        
        compatibility_data = json.loads(json_text)
    except json.JSONDecodeError as e:
        print("JSON parsing error:", e)
        compatibility_data = {
            "compatibility_score": None,
            "relationship_type": "Error",
            "common_interests": [],
            "compatibility_summary": "Failed to parse response"
        }
    except Exception as e:
        print("Gemini API error:", e)
        compatibility_data = {
            "compatibility_score": None,
            "relationship_type": "Error",
            "common_interests": [],
            "compatibility_summary": f"API request failed: {e}"
        }

    return compatibility_data


def get_gemini_subreddits(profile1_text: str) -> dict:
    prompt = f"""
    You are an expert at analyzing text-based social media profiles to evaluate interest in different communities.

    Analyze the following submission and comment text to extract the top 3 subreddits that the user is most likely interested in.

    Return your answer ONLY in structured JSON as follows:
    {{
        "Subreddit 1": string,
        "Subreddit 2": string,
        "Subreddit 3": string,
    }}

    Profile 1:
    {profile1_text[:4000]}
    """
    
    try:
        response = model.generate_content(prompt)
        #print(response)
        print(response.candidates[0].content)

        # Assume we take the first candidate's text
        raw_text = response.candidates[0].content.parts[0].text

        # Use a regex to extract the JSON inside triple backticks
        
        match = re.search(r"json\s*(\{.*\})\s*", raw_text, re.DOTALL)
        if match:
            json_text = match.group(1)
        else:
            # If the code fences aren't found, fallback to the raw text stripped.
            json_text = raw_text.strip()
        
        relevant_subreddits = json.loads(json_text)
    except json.JSONDecodeError as e:
        print("JSON parsing error:", e)
        relevant_subreddits = {
        "Subreddit 1": "",
        "Subreddit 2": "",
        "Subreddit 3": "",
        }
    except Exception as e:
        print("Gemini API error:", e)
        relevant_subreddits = {
        "Subreddit 1": "",
        "Subreddit 2": "",
        "Subreddit 3": "",
        }

    return relevant_subreddits