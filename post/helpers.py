import requests

from db import find_rows
from config import FB_GRAPH_URL
from config import FBV


    
def get_token_and_post(cp_id):
    pages = find_rows("cp_pages", {"cp_id": cp_id})
    for page in pages:
        post_to_facebook("Test message", page.page_id, page.page_token)

def post_to_facebook(message, page_id, url, access_token):
    url = f"{FB_GRAPH_URL}/{FBV}/{page_id}/photos"
    payload = {
        "url": url,
        "caption": message,
        "access_token": access_token
    }
    
    response = requests.post(url, data=payload)
    data = response.json()
    
    if "id" in data:
        print(f"Post created successfully! Post ID: {data['id']}")
    else:
        print(f"Error: {data}")