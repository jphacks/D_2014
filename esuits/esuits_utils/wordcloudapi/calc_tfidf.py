import json
from janome.tokenizer import Tokenizer
from collections import Counter
from pprint import pprint
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import boto3
from django.conf import settings

# ToDo
# ページ単位のフィルタリング
# 形態素解析
# 単語単位のフィルタリング
# (単語の正規化)
# (ストップワードの除去)
# 重要語の抽出

"""
重要語の抽出
wordsディレクトリに
重要語を頻度順に
"""

import glob
from .util import get_words_path
import sklearn
import csv


def get_words_path_list():
    words_path_list = glob.glob("./media/wordcloud/words/*.csv")
    words_path_list = [words_path.replace("\\", "/") for words_path in words_path_list]
    return words_path_list


def get_words_list():
    if settings.DEBUG:
        words_path_list = get_words_path_list()
        words_list = []
        for words_path in words_path_list:
            with open(words_path, encoding="utf-8") as f:
                reader = csv.reader(f)
                temp = []
                for line in reader:
                    temp.extend(line)
                words_list.append(temp)
        return words_list
    else:
        bucket_name = 'esuitswordcloud'
        s3 = boto3.resource('s3')
        s3client = boto3.Session().client('s3')
        words_path_list = s3client.list_objects(
            Bucket='esuitswordcloud',
            Suffix='.csv'
        )
        words_list = []
        for words_path in words_path_list:

            with open(words_path, encoding="utf-8") as f:
                reader = csv.reader(f)
                temp = []
                for line in reader:
                    temp.extend(line)
                words_list.append(temp)
        return words_list


response = s3client.list_objects(
    Bucket='hoge-bucket',
    Prefix='xx/yy/'
)


def get_now_index(url):
    words_path_list = get_words_path_list()
    now_path = get_words_path(url)
    now_index = words_path_list.index(now_path)

    return now_index


def words2doc(words):
    """
    tfidfの計算の前処理をする．wordのリストから半角スペース区切りの文章に変換
    """
    doc = " ".join(words)
    return doc


def calc_tfidf(url):
    """
    当該urlのコンテンツのtfidfを計算する．計算できない場合(n=1の場合)はdocを返す．
    """
    words_list = get_words_list()

    docs = [words2doc(words) for words in words_list]
    now_index = get_now_index(url)

    if len(docs) == 1:
        return docs[0]

    # tfidfの計算
    vectorizer = TfidfVectorizer(max_df=0.9)
    X = vectorizer.fit_transform(docs)
    words = vectorizer.get_feature_names()

    now_tfidf = X.toarray()[now_index]

    words_tfidf = {words[word_id]: tfidf for word_id,
                   tfidf in enumerate(now_tfidf) if tfidf > 10e-4}

    return words_tfidf


def main():
    with open("sample.json", encoding="utf-8") as f:
        input_json = json.load(f)
    # ページ単位のフィルタリング
    contents = [d["content"]
                for d in input_json if "/privacy/" not in d["url"] and "/en/" not in d["url"]]
    tokenizer = Tokenizer()

    word_count = Counter()
    for sentence in contents:
        print("="*50)
        # print(sentence)
        li = [token.surface for token in tokenizer.tokenize(
            sentence) if token.part_of_speech.startswith("名詞")]
        if "JavaScript" in li and ("無効" in li or "enable" in li):
            continue
        c = Counter(li)
        word_count += c
    pprint(word_count.most_common())
    from util import get_domain
    print(get_domain("https://news.yahoo.co.jp/"))


if __name__ == "__main__":
    main()
