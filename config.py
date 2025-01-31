import traceback

import yaml

config_file_path = 'env.yml'

with open(config_file_path) as stream:
    try:
        settings = yaml.safe_load(stream)
        POSTGRE_DATABASE = settings.get('pg_database')
        SECRET_KEY = settings.get('SECRET_KEY')
        IV = settings.get('IV')
        BASE_URL = settings.get('BASE_URL')
        APP_SECRET = settings.get('APP_SECRET')
        FB_GRAPH_URL = settings.get('FB_GRAPH_URL')
        FBV = settings.get('FBV')
        AD_ACCOUNT_ID = settings.get('AD_ACCOUNT_ID')
        AD_ACCOUNT_ACCESS_TOKEN = settings.get('AD_ACCOUNT_ACCESS_TOKEN')
        PAGE_ID = settings.get('PAGE_ID')
    except yaml.YAMLError:
        traceback.print_exc()