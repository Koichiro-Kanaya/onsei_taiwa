#!/usr/bin/env python3
# coding: utf-8
#
# 応答生成モジュール
# 基本的には
# - (str)nega_cnt (argv[1])
# - (str)posi_cnt (argv[2])
# - 音声認識結果が入っているファイルのパス (argv[3])
# を受け取って応答文および音声を生成する
#
# 前の応答への依存性を持たせたい場合は引数を追加すれば良い
import sys, os, subprocess
# import
from onsei_taiwa_lib.angry_siri import AngrySiri

# 音声合成エンジンのpath
#jtalkbin = '/usr/local/open_jtalk-1.07/bin/open_jtalk '
#options = ' -m syn/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /usr/local/open_jtalk-1.07/dic'

jtalkbin = 'open_jtalk '
options = '-m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic'

# 音声合成のコマンドを生成 (open jtalk を 使う場合
def mk_jtalk_command(answer):
    jtalk = 'echo "' + answer + '" | ' + jtalkbin + options + ';'
    play = 'play -q /tmp/dialogue/out.wav; rm /tmp/dialogue/out.wav;'
    return jtalk + play

if __name__ == '__main__':
    nega_cnt = int(sys.argv[1])
    posi_cnt = int(sys.argv[2])

    # 認識結果
    asrresult = open(sys.argv[3],'r') # sys.argv[3]には、ユーザの発言内容が入っている。
    question = asrresult.read().rstrip() # ユーザの発言内容
    asrresult.close()


    # インスタンスの初期化
    siri = AngrySiri()

    # 初期化メッセージを送信し、その返答を表示
    siri.init_talk() # print(siri.init_talk())

    # カスというメッセージを送信し、angryポイントを1加算し、その返答を表示
    answer, answer_ = siri.talk(question, happy_cnt=posi_cnt, angry_cnt=nega_cnt)
    print(answer) # => ('せやな！', None)

    os.system(mk_jtalk_command(answer))

