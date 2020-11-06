from .crawl_and_scrape import crawl_and_scrape
from .preprocess import preprocess

import sys

def main():
    """
    tfidfで比較する文書のwordsを事前に準備しておく
    """

    if sys.argv[1]:
        url = sys.argv[1]
    else:
        print("error")
        exit()
        
    # 入力されたurlのコンテンツを再帰的に取得する．
    contents = crawl_and_scrape(url)

    # コンテンツを形態素分析し，tfidfを計算する準備をする．
    preprocess(contents, url)

    
if __name__ == "__main__":
    main()