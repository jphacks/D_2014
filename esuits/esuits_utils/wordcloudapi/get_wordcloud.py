from wordcloud import WordCloud
import matplotlib.pyplot as plt

from .calc_tfidf import calc_tfidf
from .preprocess import preprocess
from .crawl_and_scrape import crawl_and_scrape, crawl_and_scrape_instance

from .util import get_wordcloud_path

import time

def tfidf2freqdoc(words_tfidf, doc_length=1000):
    """
    語のtfidfに応じて頻度が大きくなるような文書を返す．文書は，日本語の語をスペース区切りにしたもの．

    Args:
        words_tfidf (dict):key:語, value:語のtfidf となる辞書 {word(str):tfidf(float)}
        doc_length (int, optional): 文書の長さ. Defaults to 1000.
    """
    # tfidfの和が1になるように正規化し，語数に換算する．
    tfidf_sum = sum(words_tfidf.values())
    words_freq = {word : int(doc_length * tfidf / tfidf_sum) for word, tfidf in words_tfidf.items()}

    # スペース区切りのドキュメントに変換
    freqdoc = " ".join([" ".join([word] * count) for word, count, in words_freq.items()])

    return freqdoc


def get_wordcloud(url):
    # 入力されたurlのコンテンツを再帰的に取得する．
    # contents = crawl_and_scrape(url)
    start_time = time.time()
    contents = crawl_and_scrape_instance(url)
    crawl_end_time = time.time()
    print()
    print("crawl & scrape time:", crawl_end_time - start_time, "seconds")
    print()

    if contents is None:
        return "error"

    # コンテンツを形態素分析し，tfidfを計算する準備をする．
    preprocess(contents, url)
    
    keitaiso_end_time = time.time() 
    print()
    print("形態素解析 time:",keitaiso_end_time - crawl_end_time, "seconds")
    print()

    # 単語ごとのtfidfを計算する．
    words_tfidf = calc_tfidf(url)
    
    tfidf_end_time = time.time()
    print()
    print("tfidf time:",tfidf_end_time - keitaiso_end_time, "seconds")
    print()

    # 各単語語のtfidfに比例する語数の文章を作る．

    # tf-idfを計算できなかった場合はdocが帰ってきている．
    if type(words_tfidf) == str:
        freqdoc = words_tfidf
    else:
        # tf-idfを計算できなかった場合
        freqdoc = tfidf2freqdoc(words_tfidf)
    
    freq_end_time = time.time()

    # ワードクラウドの作成
    font_path = "./static/esuits/fonts/NotoSansCJKjp-Regular.otf"
    word_cloud = WordCloud(font_path=font_path, background_color="white").generate(freqdoc)
    
    output_path = get_wordcloud_path(url)

    from .util import get_domain
    # output_path = "./static/esuits/images/" + get_domain(url) + ".png"
    # output_path = "./media/wordcloud/wordclouds/www.bandainamco-mirai.com.png"
    word_cloud.to_file(output_path)

    cloud_end_time = time.time()
    print()
    print("wordcloud time", cloud_end_time - freq_end_time, "seconds")
    print()
    return output_path


def main():

    url = "https://news.yahoo.co.jp/"
    
    import sys
    if len(sys.argv) == 2:
        url = sys.argv[1]

    get_wordcloud(url)
    
if __name__ == "__main__":
    main()