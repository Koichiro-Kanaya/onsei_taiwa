# coding: utf_8
# 音声対話システムデモ

# めも
# ・asrresult.txtは自分が言った内容が入っている。(ex.今日のあれは？

import os
import subprocess
import sys

# 悪い言葉のリストを作成する。
nega_wordslist = ['ゴミ', 'カス']
posi_wordslist = ['ありがとう', '感謝']

# dialogue directory
tmpdirname = './tmp/dialogue'

# もしディレクトリが存在しなければ作成
if os.path.isdir(tmpdirname) == False:
    os.mkdir('./tmp')
    os.mkdir(tmpdirname)


def main():
    while True:
        # inputファイルを定義
        filename = tmpdirname + '/input.wav'
        subprocess.call('adinrec ' + filename + ' > /dev/null', shell=True)

        #話者認識
        sidfile = tmpdirname + '/spkid.txt'
        subprocess.call('touch ' + sidfile, shell=True)
        subprocess.call('./sid/test.sh ' + filename + ' '+ sidfile, shell=True)

        # 現在の話者番号を取得
        # もし前の状態を保存しておきたければ、別変数/別ファイルを用意する
        with open(sidfile, 'r') as f:
            sidnum = f.read().strip('\n')

        # 音声認識
        asrresult = tmpdirname + '/asrresult.txt'
        with open(tmpdirname + '/list.txt', mode='w') as f:
            f.write(filename)
        
        # 音声認識をして結果をファイルに保存
	    # もし前の状態を保存しておきたければ別変数/別ファイルを用意する
        subprocess.call('julius -C asr/grammar.jconf -filelist ' + tmpdirname + '/list.txt 2> /dev/null | grep "^sentence1: " | sed -e "s/sentence1://" -e "s/silB//" -e "s/silE//" -e "s/ //g" > ' + asrresult, shell = True)
        subprocess.call('rm ./' + tmpdirname + '/list.txt', shell = True)


        # 自分の発言にnega/posi発言が何個ずつあるかを取得する。
        nega_cnt = 0
        posi_cnt = 0
        with open(asrresult, 'r') as f:
            sentence = f.read().strip('\n')
        # 悪い言葉をカウント
        for index in range(len(nega_wordslist)):
            if nega_wordslist[index] in sentence:
                nega_cnt += 1
        # いい言葉をカウント
        for index in range(len(posi_wordslist)):
            if posi_wordslist[index] in sentence:
                posi_cnt += 1


        # 話者認識/音声認識結果を応答を生成する
        # 状態/履歴への依存性を持たせたければこのプログラムを適宜修正（引数変更等）
        # 初期では話者ID を元に異なる応答リストを読み込む仕様
        subprocess.call('./response.py ' + str(nega_cnt) + ' ' + str(posi_cnt) + ' ' + asrresult, shell = True)


        #事後処理
        subprocess.call('rm ' + filename + ' ' + sidfile + ' ' + asrresult, shell = True)

        

# Ctrl-C で抜けるための処理
try:
    main()
except KeyboardInterrupt:
    os.system('rm -r ' + tmpdirname)
    os.system('rm -r ./tmp')
    sys.exit(0)