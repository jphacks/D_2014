from multiprocessing import Process, Pipe
import scrapy
from scrapy.http import Response
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from twisted.internet import reactor
from .util import get_content, get_contents_path, get_domain, get_unique_id

from django.conf import settings

import boto3

import os
import json
import logging


class Page(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    text = scrapy.Field()
    pass


class MySpider(CrawlSpider):
    name = 'my_spider'

    rules = (
        Rule(LinkExtractor(), callback="parse", follow=True),
    )

    def __init__(self, urls, *args, **kwargs):
        # ログ抑制
        logging.getLogger("scrapy").setLevel(logging.WARNING)

        self.start_urls = urls

        # 最初に入力したurlのドメインのみクロール対象にする．
        self.allowed_domains = [get_domain(url) for url in urls]

        super(MySpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        # ページからコンテンツを取得する
        title, text = get_content(response.text)
        url = response.url
        yield Page(url=url, title=title, text=text)


def crawl():
    pass


def work(conn, url):
    contents = crawl_and_scrape(url)
    conn.send(contents)
    conn.close()
    return


def crawl_and_scrape_instance(url):
    # 同一プロセスだと複数回クロールできないっぽいので別プロセスを作る(何か他に良い方法ありそう)

    par_conn, child_conn = Pipe()

    p = Process(target=work, args=(child_conn, url))

    p.start()
    contents = par_conn.recv()
    p.join()

    return contents


def crawl_and_scrape(url):
    """
    入力されたurlを起点に,再帰的にページをクロールし，取得した文章コンテンツを返す．

    Args:
        url (str): 再帰的クロールを開始するurl．

    Returns:
        (list): 取得したコンテンツのリスト．コンテンツは辞書形式:{"url":str, "title":str, "text":str}
    """

    # output_pathはurlのドメインに
    if settings.DEBUG:
        output_path = get_contents_path(url)
    else:
        output_name = get_unique_id(url) + '.json'
        output_path = '/tmp/' + output_name
        bucket_name = 'esuitswordcloud'
        s3 = boto3.resource('s3')

    # 既に当該ドメインをクロール済みの場合
    if os.path.exists(output_path):
        try:
            with open(output_path, encoding="utf-8") as f:
                contents = json.load(f)
                return contents
        except:
            os.remove(output_path)

    settings = {
        # "USER_AGENT":"",
        "EXTENSIONS": {
            #    'scrapy.extensions.telnet.TelnetConsole': None,
            'scrapy.extensions.closespider.CloseSpider': 1,
        },
        "CLOSESPIDER_TIMEOUT": 0,
        "CLOSESPIDER_ITEMCOUNT": 30,
        "CLOSESPIDER_PAGECOUNT": 0,
        "CLOSESPIDER_ERRORCOUNT": 0,
        "CONCURRENT_REQUESTS": 16,
        "DOWNLOAD_DELAY": 1,  # リクエストの間隔
        "DEPTH_LIMIT": 2,  # 再帰の深さ上限
        "FEED_FORMAT": "json",
        "FEED_URI": output_path,  # 出力ファイルパス
        "FEED_EXPORT_ENCODING": 'utf-8',
    }

    print("crawl start")

    # クローリング実行
    # process: CrawlerProcess = CrawlerProcess(settings=settings)
    # process.crawl(MySpider, [url])
    # process.start()  # the script will block here until the crawling is finished

    runner:  CrawlerRunner = CrawlerRunner(settings=settings)
    d = runner.crawl(MySpider, [url])
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # クロールが終了するまでスクリプトはここでブロックされます

    if not settings.DEBUG:
        s3.Bucket(bucket_name).upload_file(output_path, output_name)

    # スクレイピング結果はoutput_pathに保存してある．
    try:
        with open(output_path, encoding="utf-8") as f:
            contents = json.load(f)
    except:
        contents = None

    print("crawl end")

    return contents


def main():
    settings = {
        # "USER_AGENT":"",
        "CONCURRENT_REQUESTS": 16,
        "DOWNLOAD_DELAY": 1,  # リクエストの間隔
        "DEPTH_LIMIT": 2,  # 再帰の深さ上限
        "FEED_FORMAT": "json",
        "FEED_URI": "./sample.json",  # 出力ファイルパス
        "FEED_EXPORT_ENCODING": 'utf-8',
    }

    # クローリング実行
    process: CrawlerProcess = CrawlerProcess(settings=settings)
    process.crawl(MySpider, ["https://news.yahoo.co.jp/"])
    process.start()  # the script will block here until the crawling is finished


if __name__ == "__main__":
    main()
