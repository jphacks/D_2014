"""ニュースを取ってくる関数"""
import urllib.parse
import feedparser
from typing import List

def get_news(q:str, country:str = 'jp') -> List:
    """検索ワードと国を入力すると関連するニュースを返す関数。

    Args:
        q (str): 検索ワード
        country (str, optional): 国名、言語. Defaults to 'jp'.

    Returns:
        List: ニュースが格納されたリスト。各ニュースは{'title':'','url':''}形式。
    """
    endpoint = 'http://news.google.com/news?'
    qdict = {
        'q' : q,
        'ned' : country,
        'hl' : country,
        'output' : 'rss',
    }
    RSS_URL = endpoint + urllib.parse.urlencode(qdict)
    news = feedparser.parse(RSS_URL)
    news_list = []
    for entry in news.entries:
        news_list.append({'title':entry.title, 'url':entry.link})
    
    return news_list
