from django.shortcuts import render
from .forms import ChangeColorForm
from django.http.response import JsonResponse
from typing import List


def change_color_sample(request):
    ES = request.GET.get('ES','')
    if ES:
        modeified_ES = modify_ES(ES)
        return JsonResponse({"ES":modeified_ES})
    form = ChangeColorForm()
    return render(request,'samples/change_color_sample.html', {'form':form})

def modify_ES(ES:str) -> List:
    """ES添削用の関数のサンプル。この関数では「です。」を赤色にする。
    背景色を変えるか文字の色を変えるかはhtml側に任せる。
    コーナーケースがあるけど面倒だから無視。

    Args:
        ES (str): エントリーシートの文章全体

    Returns:
        List: 文章のリスト。各要素は{part:文章の一部, color:その文章の色(htmlで使用できるもの)}。色がない場合はとりあえず"None"を入れているけど要検討。
    """
    res = []
    ES = ES.split('です。')
    for part in ES:
        res.append({'part':part, 'color':'None'})
        res.append({'part':'です。', 'color':'red'})

    return res
