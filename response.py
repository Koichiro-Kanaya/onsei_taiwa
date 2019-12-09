#!/usr/bin/env python3
# coding: utf-8
#
# 応答生成モジュール
import sys, os, subprocess

# 音声合成エンジンのpath
#jtalkbin = '/usr/local/open_jtalk-1.07/bin/open_jtalk '
#options = ' -m syn/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /usr/local/open_jtalk-1.07/dic'

jtalkbin = 'open_jtalk '

# メンバーリスト
member_list = ['藤村', '金谷', '鈴木', '陳']

# 音声合成のコマンドを生成
def mk_jtalk_command(answer, mode):
    if mode == 'happy':
        options = '-m ./MMDAgent_Example-1.8/Voice/mei/mei_happy.htsvoice -ow ./tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic'
    elif mode == 'angry':
        options = '-m ./MMDAgent_Example-1.8/Voice/takumi/takumi_angry.htsvoice -ow ./tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic'
    else:
        options = '-m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow ./tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic'

    jtalk = 'echo "' + answer + '" | ' + jtalkbin + options + ';'
    play = 'play -q ./tmp/dialogue/out.wav; rm ./tmp/dialogue/out.wav;'
    return jtalk + play

def response_gen(siri, question, nega_cnt, posi_cnt, sidnum):
    # カスというメッセージを送信し、angryポイントを1加算し、その返答を表示
    answer, changeMode = siri.talk(member_list[int(sidnum) - 1], question, happy_cnt=posi_cnt, angry_cnt=nega_cnt)
    if answer == 'NOMATCH':
        if siri.get_mode(member_list[int(sidnum) - 1]) == 'angry':
            answer = '何を言っているかよくわかりませんハゲ野郎'
        elif siri.get_mode(member_list[int(sidnum) - 1]) == 'happy':
            answer = 'あなたのおっしゃっていることが分かりませんので、もう一度言い直してくださいませんか、ご主人様'
        else:
            answer = 'もう一度言い直してください。'
    print('Siri(' + siri.get_mode(member_list[int(sidnum) - 1]) + 'モード) : ' + answer) # => ('せやな！', None)

    if changeMode != None:
        if siri.get_mode(member_list[int(sidnum) - 1]) == 'angry':
            changeMode = '怒りました。'
        elif siri.get_mode(member_list[int(sidnum) - 1]) == 'happy':
            changeMode = member_list[int(sidnum) - 1] + 'さんが大好きです。'
        else:
            changeMode = 'モードが切り替わりました。'
    print(member_list[int(sidnum) - 1] + 'さんの現在のスコア : ' + str(siri[member_list[int(sidnum) - 1]].score))
    print('posi_cnt : ' + str(posi_cnt))
    print('nega_cnt : ' + str(nega_cnt))
    print('-------------------------')

    if changeMode == None:
        os.system(mk_jtalk_command(answer, siri.get_mode(member_list[int(sidnum) - 1])))
    else:
        os.system(mk_jtalk_command(answer + changeMode, siri.get_mode(member_list[int(sidnum) - 1])))

