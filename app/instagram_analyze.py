import requests
from pandas.io.json import json_normalize
import pandas as pd

from _config import INSTAGRAM_CLIENT_ID


def instagram_analyzer(query):
    base_url = "https://api.instagram.com/v1"
    url = '{0}/tags/{1}/media/recent?client_id={2}&count=30'.format(
        base_url, query, INSTAGRAM_CLIENT_ID)
    request = requests.get(url)
    json_results = request.json()
    results = []
    if 'data' in json_results:
        data = json_results['data']
        df_instance = json_normalize(data)
        results.append(df_instance)

    df = pd.DataFrame().append(results)

    cols = [
        'comments.count',
        'likes.count',
    ]
    df_cols = df[cols]
    df_clean = df_cols.rename(columns=lambda x: x.replace('.', ' ').title())

    return df_clean
