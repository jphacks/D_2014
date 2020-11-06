import json
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *

import os
import csv
from .util import get_words_path

class NumericReplaceFilter(TokenFilter):
    """
    名詞と判断された(漢)数字を全て0に置換
    """
    def apply(self, tokens):
        for token in tokens:
            parts = token.part_of_speech.split(',')
            if (parts[0] == '名詞' and parts[1] == '数'):
                token.surface = '0'
                token.base_form = '0'
                token.reading = 'ゼロ'
                token.phonetic = 'ゼロ'
            yield token

def js_check_page(text):
    return "JavaScript" in text and ("無効" in text or "enable" in text)

def page_level_filtering(contents):
    """
    ページ単位で弾くべきものを弾く
    """

    # プライバシーポリシー，お問い合わせページ，英語ページを取り除く
    exclude_list = ["/privacy/","/inquiry/", "/en/"]
    for word in exclude_list:
        contents = [c for c in contents if word not in c["url"]]
    
    # Javascriptを有効にしてくださいページを取り除く
    contents = [c for c in contents if not js_check_page(c["text"])]

    return contents

def delite_stopwords(words):
    words = [word for word in words if "0" not in word]
    return words

def preprocess(contents, url):
    """
    スクレイピングした文章コンテンツに対し，特徴語抽出するために種々の前処理を行う．
    前処理後は単語のリストをcsvで保存する．

    Args:
        contents (list): コンテンツのリスト．コンテンツは辞書形式:{"url":str, "title":str, "text":str}
    """

    output_path = get_words_path(url)

    # 既に前処理済みの場合
    if os.path.exists(output_path):
        return

    # ページ単位のフィルタリング
    contents = page_level_filtering(contents)

    # Unicodeを正規化することで表記ゆれを吸収するフィルター
    char_filters = [UnicodeNormalizeCharFilter()]

    # 数値を全て0にする, 名詞が連続->複合名詞を作る, [名詞, 動詞, 形容詞, 副詞]のみ取得する
    token_filters = [NumericReplaceFilter(), CompoundNounFilter(), POSKeepFilter(["名詞", "動詞", "形容詞", "副詞"])]

    # 形態素解析
    tokenizer = Tokenizer()
    analyzer = Analyzer(char_filters=char_filters, tokenizer=tokenizer, token_filters=token_filters)

    words = []
    print("形態素解析スタート")
    for content in contents:
        temp_words = [token.surface for token in analyzer.analyze(text=content["text"])]
        words.extend(temp_words)

    print("形態素解析終了")

    # ストップワードの除去(未対応)
    words = delite_stopwords(words)
    
    # 保存
    with open(output_path, "w",  encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(words)
    
    return

def main():
    pass

if __name__ == "__main__":
    main()