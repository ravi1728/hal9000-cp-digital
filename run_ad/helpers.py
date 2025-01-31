from datetime import datetime
import pytz
import requests
import json
from config import AD_ACCOUNT_ID
from config import AD_ACCOUNT_ACCESS_TOKEN
from config import FB_GRAPH_URL
from config import FBV
from config import PAGE_ID


FB_BASE_URL = f"{FB_GRAPH_URL}/{FBV}"

def run_fb_add_helper(cp_id, lead_form_link, creative_url):
    campaign_id = create_facebook_campaign()
    ad_set_id = create_ad_set(campaign_id)
    creative_id = create_ad_creative(lead_form_link, creative_url)
    create_ad(ad_set_id, creative_id)




def create_facebook_campaign():
    url = f"{FB_BASE_URL}/{AD_ACCOUNT_ID}/campaigns"
    dt  = datetime.now()
    ist_timezone = pytz.timezone("Asia/Kolkata")
    ist_time = dt.astimezone(ist_timezone)
    time_str = ist_time.strftime("%Y-%m-%d %H:%M:%S")
    payload = {
        "name": f"CP Campaign - {time_str}",
        "objective": "CONVERSIONS",
        "status": "ACTIVE",
        "access_token": AD_ACCOUNT_ACCESS_TOKEN
    }

    response = requests.post(url, data=payload)
    result = response.json()
    
    if "id" in result:
        campaign_id = result["id"]
        print(f"Campaign Created: {campaign_id}")
        return campaign_id
    else:
        print(f"Error Creating Campaign: {result}")
        return None


def create_ad_set(campaign_id):
    url = f"{FB_BASE_URL}/{AD_ACCOUNT_ID}/adsets"
    payload = {
        "name": "Static Ad Set",
        "campaign_id": campaign_id,
        "targeting": json.dumps({
            "geo_locations": {"countries": ["IN"]},
            "age_min": 30,
            "age_max": 45
        }),
        "optimization_goal": "LINK_CLICKS",
        "billing_event": "IMPRESSIONS",
        "daily_budget": "1000",
        "status": "ACTIVE",
        "access_token": AD_ACCOUNT_ACCESS_TOKEN
    }

    response = requests.post(url, data=payload)
    result = response.json()
    
    if "id" in result:
        ad_set_id = result["id"]
        print(f"Ad Set Created: {ad_set_id}")
        return ad_set_id
    else:
        print(f"Error Creating Ad Set: {result}")
        return None


def create_ad_creative(lead_form_link, creative_url):
    url = f"{FB_BASE_URL}/{AD_ACCOUNT_ID}/adcreatives"
    payload = {
        "name": "Static Ad Creative",
        "object_story_spec": json.dumps({
            "page_id": PAGE_ID,
            "link_data": {
                "message": "Check out our amazing offer!",
                "link": lead_form_link,
                "name": "Special Discount!",
                "description": "Limited-time offer. Don't miss out!",
                "picture": creative_url,
            }
        }),
        "access_token": AD_ACCOUNT_ACCESS_TOKEN
    }

    response = requests.post(url, data=payload)
    result = response.json()
    
    if "id" in result:
        creative_id = result["id"]
        print(f"Ad Creative Created: {creative_id}")
        return creative_id
    else:
        print(f"Error Creating Ad Creative: {result}")
        return None


def create_ad(ad_set_id, creative_id):
    url = f"{FB_BASE_URL}/{AD_ACCOUNT_ID}/ads"
    payload = {
        "name": "Static Ad",
        "adset_id": ad_set_id,
        "creative": json.dumps({"creative_id": creative_id}),
        "status": "ACTIVE",
        "access_token": AD_ACCOUNT_ACCESS_TOKEN
    }

    response = requests.post(url, data=payload)
    result = response.json()
    
    if "id" in result:
        ad_id = result["id"]
        print(f"Ad Created: {ad_id}")
    else:
        print(f"Error Creating Ad: {result}")