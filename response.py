#!/usr/bin/env python3
# coding: utf-8
#
# 応答生成モジュール
# 基本的には
# - (str)nega_cnt (argv[1])
# - (str)posi_cnt (argv[2])
# - 発言した人の番号 (argv[3])
# - 音声認識結果が入っているファイルのパス (argv[4])
# を受け取って応答文および音声を生成する
#
# 前の応答への依存性を持たせたい場合は引数を追加すれば良い
import sys, os, subprocess

# 音声合成エンジンのpath
#jtalkbin = '/usr/local/open_jtalk-1.07/bin/open_jtalk '
#options = ' -m syn/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /usr/local/open_jtalk-1.07/dic'

jtalkbin = 'open_jtalk '
options = '-m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow ./tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic'

# 音声合成のコマンドを生成
def mk_jtalk_command(answer):
    jtalk = 'echo "' + answer + '" | ' + jtalkbin + options + ';'
    play = 'play -q ./tmp/dialogue/out.wav; rm ./tmp/dialogue/out.wav;'
    return jtalk + play

def response_gen(siri, question, nega_cnt, posi_cnt, sidnum):
    # カスというメッセージを送信し、angryポイントを1加算し、その返答を表示
    answer, _ = siri.talk(question, happy_cnt=posi_cnt, angry_cnt=nega_cnt)
    print('Siri   : ' + answer) # => ('せやな！', None)
    print('-------------------------')
    print(siri.score)
    print(posi_cnt)
    print(nega_cnt)

    os.system(mk_jtalk_command(answer))

