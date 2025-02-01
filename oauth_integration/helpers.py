from urllib.parse import urlencode
import requests
from config import BASE_URL
from config import APP_SECRET
from config import FB_GRAPH_URL
from config import FBV
from db import create_or_update_row
from utils.encryption import encrypt

def fb_oauth_helper(code, state):
    app_id, cp_id = state.split(",")
    redirect_uri = f"{BASE_URL}/fb-oauth"
    access_token = get_access_token_from_fb(app_id, redirect_uri, APP_SECRET,
                                            code)
    user_token = get_user_token(app_id, APP_SECRET, access_token)
    save_user_token(user_token, cp_id)
    update_user_accessible_pages(user_token, cp_id)

def get_access_token_from_fb(app_id, redirect_uri, app_secret, code):
    url = (f"{FB_GRAPH_URL}/oauth/access_token?"
           f"client_id={app_id}&redirect_uri={redirect_uri}&"
           f"client_secret={app_secret}&code={code}")
    data = requests.get(url).json()
    return data.get('access_token')

def get_user_token(app_id, app_secret, access_token):
    url = (
        f"{FB_GRAPH_URL}/{FBV}/oauth/access_token?"
        f"grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}"
        f"&fb_exchange_token={access_token}")
    data = requests.get(url).json()
    return data.get('access_token')

def save_user_token(user_token, cp_id):
    create_or_update_row("cp_users_hal9000", {'user_token': encrypt(user_token), 'cp_id': cp_id}, ["cp_id"])

def update_user_accessible_pages(user_token, cp_id):
    pages = get_user_accessible_pages(user_token)
    page_ids = [page['id'] for page in pages]
    for page_id in page_ids:
        try:
            page_data = get_fb_page_data(page_id, user_token)
            subscribe_app_to_page(page_id, page_data["access_token"])
            fb_page_dict = {
                'page_id': page_id,
                'page_name': page_data['name'],
                'page_token': encrypt(page_data['access_token']).decode("utf-8"),
            }
            create_or_update_row("fb_pages_hal9000", fb_page_dict, ["page_id"])
            create_or_update_row("cp_pages_hal9000", {'page_id': page_id, 'cp_id': cp_id}, ["page_id", "cp_id"])
        except Exception as e:
            print(f"error adding fb page {page_id} - ", e)


def get_user_accessible_pages(user_token):
    url = f"{FB_GRAPH_URL}/{FBV}/me/accounts"
    params = {
        'access_token': user_token,
        'fields': 'id,name',
        'limit': 10000,
    }
    url = f"{url}?{urlencode(params)}"
    res = requests.get(url).json()
    return res['data']


def get_fb_page_data(page_id, user_token=None):
    url = f"{FB_GRAPH_URL}/{FBV}/{str(page_id)}"
    params = {
        'access_token': user_token,
        'fields': 'name, id, access_token',
    }
    url = f"{url}?{urlencode(params)}"
    return requests.get(url).json()


def subscribe_app_to_page(
    page_id,
    page_token,
):
    post_url = (
        f"{FB_GRAPH_URL}/{FBV}/{str(page_id)}/subscribed_apps"
    )
    fields_to_subscribe = "feed"
    params = {
        'access_token': page_token,
        'subscribed_fields': fields_to_subscribe
    }
    post_url = f"{post_url}?{urlencode(params)}"
    requests.post(post_url)