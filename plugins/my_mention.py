from slackbot.bot import listen_to, respond_to, settings, default_reply

g_status = {
    'count_list':[],
    'attendee_list': [],
    'absentee_list': [],
}

#YESと判断されるメッセージリスト
YES_MESSAGE_LIST = ['まる']
#YES(実質)と判断されるメッセージリスト
SIKATANAI_MESSAGE_LIST = ['さんかく']
#NOと判断されるメッセージリスト
NO_MESSAGE_LIST = ['ばつ']
#もとのカウント  24はスタッフの人数
original_count = [3 for i in range(24)]
#count_statusの置き換え用
sub = {}


#指定されたSlackのuser id に対応する username を返す
def _get_user_name(message):
    """
    :param message:
    :return: str or None
    """
    user = message.body.get('user')
    if not user:
        return None
    user_name = message.channel._client.users[user]['name']
    return user_name

#'カウント'に反応してメッセージ送信
@respond_to('カウント')
def start(message):
    message.send('皆さん今回のイベントいけますか？いける方は　{}　仕方のない理由でいけない方は　{}　普通にいけない方は　{}　とコメントお願いします。'.format('か'.join(YES_MESSAGE_LIST),'か'.join(SIKATANAI_MESSAGE_LIST),'か'.join(NO_MESSAGE_LIST)))


#リプに対してスタンプしてリストに入れる。
@listen_to('.+')
@respond_to('.+')
def listen(message):
    send_user = _get_user_name(message)
    if send_user:
        message_text = message.body['text']
        if message_text in YES_MESSAGE_LIST:
                g_status['count_list'].append('<@{}>'.format(send_user))
                g_status['attendee_list'].append('<@{}>'.format(send_user))
                message.react('+1')
        elif message_text in SIKATANAI_MESSAGE_LIST:
                g_status['count_list'].append('<@{}>'.format(send_user))
                g_status['attendee_list'].append('<@{}>'.format(send_user))
                message.react('+1')
        elif message_text in NO_MESSAGE_LIST:
                g_status['count_list'].append('<@{}>'.format(send_user))
                g_status['absentee_list'].append('<@{}>'.format(send_user))
                message.react('+1')
    else:
        message.send('誰？')

#'終了'に反応してカウントする
@respond_to('終了')
def end(message):
    message.send('カウントします！')

#カウントを辞書式にして設定する。key,value の順
    count_list = g_status['count_list']
    print(count_list)
    count_status = dict(zip(count_list,original_count))

#出席、欠席リストを簡略化
    attendee_list = g_status['attendee_list']
    absentee_list = g_status['absentee_list']

#key(staff),value(count)からできている辞書から欠席分を引き算
    #subがグローバルであることを示す
    global sub 
    #初回
    if sub == {}:
        for absentee in absentee_list:
            count_status[absentee] -= 1
    
        for attendee in attendee_list:
            count_status[attendee] += 0

        for k,v in count_status.items():
            message.send('{} 残りカウントは{}です。'.format(str(k),str(v)))
    #2回目以降   
    else:
        for absentee in absentee_list:
            sub[absentee] -= 1
    
        for attendee in attendee_list:
            sub[attendee] += 0

        for k,v in sub.items():
            message.send('{} 残りカウントは{}です。'.format(str(k),str(v)))
    
    #置き換え
    if sub == {}:
        sub = count_status.copy()
    

    #リストのクリア
    g_status['attendee_list'] = []
    g_status['absentee_list'] = []  
    g_status['count_list'] = []
    attendee_list = []   
    absentee_list = []
    count_list = []