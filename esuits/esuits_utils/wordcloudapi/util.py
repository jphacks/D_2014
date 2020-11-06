import logging

import lxml.html
import readability

import os
from urllib.parse import urlparse


CONTENTS_ROOT = "./media/wordcloud/contents/"
WORDS_ROOT = "./media/wordcloud/words/"
WORDCLOUD_ROOT = "./media/wordcloud/wordclouds/"

for ROOT in [CONTENTS_ROOT, WORDS_ROOT, WORDCLOUD_ROOT]:
    try:
        os.makedirs(ROOT)
        print("created :", ROOT)
    except FileExistsError:
        pass

# readability君がデフォルトのままだとDEBUG,INFOレベルのログを大量に出すので抑制
logging.getLogger("readability.readability").setLevel(logging.WARNING)

def get_content(html):
    """
    HTMLから，タプルとして(タイトル, 本文)を取り出す．
    """
    document = readability.Document(html)
    content_html = document.summary()

    content_text = lxml.html.fromstring(content_html).text_content().strip()
    title = document.short_title()

    return title, content_text


def get_contents_path(url):
    # contentのパスはドメインにunique
    # domain = get_domain(url)
    # contents_path = os.path.join(CONTENTS_ROOT, domain) + ".json"
    unique_id = get_unique_id(url)
    contents_path = os.path.join(CONTENTS_ROOT, unique_id) + ".json"
    return contents_path

def get_words_path(url):
    # domain = get_domain(url)
    # words_path = os.path.join(WORDS_ROOT, domain) + ".csv"
    unique_id = get_unique_id(url)
    words_path = os.path.join(WORDS_ROOT, unique_id) + ".csv"
    return words_path

def get_wordcloud_path(url):
    # domain = get_domain(url)
    # wordcloud_path = os.path.join(WORDCLOUD_ROOT, domain) + ".png"
    unique_id = get_unique_id(url)
    wordcloud_path = os.path.join(WORDCLOUD_ROOT, unique_id) + ".png"
    
    return wordcloud_path

def get_domain(url):
    res = urlparse(url)
    return res.netloc

def get_unique_id(url):
    unique_id = url.replace(":", "_").replace("/", "_")
    return unique_id