#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import itertools as it
import re
import pickle
from optparse import OptionParser

usage = u"""usage: %prog datafile 
アクセント句境界推定用に特徴量追加して出力"""
parser = OptionParser(usage=usage)
(options,args) = parser.parse_args()

if len(args) < 1:
    print >> sys.stderr, "Error: too few arguments\n"
    parser.print_help()
    exit()

datafile = open(args[0])

#gram21 = pickle.load( open("./2gram1.dat") )
#gram22 = pickle.load( open("./2gram2.dat") )
#gram23 = pickle.load( open("./2gram3.dat") )
#gram24 = pickle.load( open("./2gram4.dat") )

renoun = re.compile("名詞")

# 入力のデータファイルのフォーマット
#
# 0.書字形, 1.発音形, 2.品詞, 3.活用型, 4.活用形, 5.語彙素-語彙素読み,
# 6.語種, 7.語頭変化結合型 8.アクセントタイプ, 9.アクセント結合型, 10.アクセント修飾型,
# 11.IREX, 12.文節
#
# 0.orth, 1.pron, 2.pos, 3.cType, 4.cForm, 5.lemma,
# 6.goshu, 7.iType, 8.aType, 9.aConType, 10.aModType,
# 11.irex, 12.bunsetu

# ラベルファイルのフォーマット
# 0.書字形, 1.発音形, 2.文中アクセント, 3.アクセント句境界
# 0.L_orth, 1.L_pron, 2.L_accent 3.L_boundary

# ここで追加する素性
#
# 当該形態素のモーラ数 nmora
# 2-noungram スコア（1-5）があれば、その値 s2noungram[1-4]
# [1-4] では、正規化の仕方が異なる。

# それ自身ではモーラ数にカウントされない読み一覧
nonMoraList = set(u"ァ ィ ゥ ェ ォ ャ ュ ョ".split())

prevorth = ""
previsnoun = 0

for dataline in datafile:

    # ここにデータをすべて保存する
    data = {}

    # 空行のデータは読まずに空行を出力して終わる
    if len(dataline.strip()) == 0:
        print
        prevorth = ""
        previsnoun = 0
        continue

    # データを読む
    data["orth"], data["pron"], data["pos"], data["cType"], data["cForm"], \
    data["lemma"], data["goshu"], data["iType"], data["aType"], data["aConType"], \
    data["aModType"], data["irex"], data["bunsetsu"] = dataline.split()
    
    # 発音形 pron をモーラごとに分ける
    index_mora = 0
    mora = []
    for p in data["pron"].decode("utf-8"):
        if p not in nonMoraList:
            mora.append(p.encode("utf-8"))
            index_mora += 1
        else:
            mora[index_mora-1] += p.encode("utf-8")

    # nmora を追加
    data["nmora"] = str(len(mora))
    
    # CRF++ のデータ形式で出力する
    print data["orth"],
    print data["pron"],
    print data["pos"],
    print data["cType"],
    print data["cForm"],
    print data["lemma"],
    print data["goshu"],
    print data["iType"],
    print data["aType"],
    print data["aConType"],
    print data["aModType"],
    print data["irex"],
    print data["bunsetsu"],
    print data["nmora"]

