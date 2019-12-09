# coding: utf_8
# 音声対話システムデモ

# めも
# ・asrresult.txtは自分が言った内容が入っている。(ex.今日のあれは？)

import os
import subprocess
import sys
from response import response_gen
from onsei_taiwa_lib.angry_siri import AngrySiri
from onsei_taiwa_lib.angry_siri import MultiAngrySiri


# 悪い言葉リストの作成
nega_wordslist = []
with open('./nega_word.txt') as f:
    for line in f:
        nega_wordslist.append(line.rstrip('\n'))
# 良い言葉リストの作成
posi_wordslist = []
with open('./posi_word.txt') as f:
    for line in f:
        posi_wordslist.append(line.rstrip('\n'))

# メンバーリスト
member_list = ['藤村', '金谷', '鈴木', '陳']

# dialogue directory
tmpdirname = './tmp/dialogue'

# もしディレクトリが存在しなければ作成
if os.path.isdir(tmpdirname) == False:
    os.mkdir('./tmp')
    os.mkdir(tmpdirname)


def main():
    # インスタンスの初期化
    # siri = AngrySiri()
    siri = MultiAngrySiri(member_list, load_pickle=False)

    # 初期化メッセージを送信し、その返答を表示
    siri.init_talks() # print(siri.init_talk())
    
    try:
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

            print("あなたは" + member_list[int(sidnum) - 1] + "さんですね！")

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
                question = f.read().strip('\n')
                # ユーザの言葉を表示する
                print('あなた : ' + question)
        

            # 悪い言葉をカウント
            for index in range(len(nega_wordslist)):
                for i in range(len(question) - len(nega_wordslist[index]) + 1):
                    if nega_wordslist[index] == question[i:i+len(nega_wordslist[index])]:
                        nega_cnt+=1
            # いい言葉をカウント
            for index in range(len(posi_wordslist)):
                for i in range(len(question) - len(posi_wordslist[index]) + 1):
                    if posi_wordslist[index] == question[i:i+len(posi_wordslist[index])]:
                        posi_cnt+=1

            # 話者認識/音声認識結果を応答を生成する
            # 状態/履歴への依存性を持たせたければこのプログラムを適宜修正（引数変更等）
            # 話者ID を元に異なる応答リストを読み込む仕様

            # 認識結果
            response_gen(siri, question, nega_cnt, posi_cnt, sidnum)


            #事後処理
            subprocess.call('rm ' + filename + ' ' + sidfile + ' ' + asrresult, shell = True)

    # Ctrl-C で抜けるための処理
    except KeyboardInterrupt:
        os.system('rm -r ' + tmpdirname)
        os.system('rm -r ./tmp')
        siri.save()
        sys.exit(0)


main()
