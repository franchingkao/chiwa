from linebot.models import MessageEvent, TextMessage, TextSendMessage, ConfirmTemplate, MessageAction, TemplateSendMessage, QuickReply, QuickReplyButton, ButtonsTemplate, URIAction
import datetime
from dateutil import parser
import copy, json
from collections import defaultdict
import os

def firstMeet():
    buttons_template = ButtonsTemplate(
        title='在路上遇到了一隻小吉!',
        thumbnail_image_url='https://firebasestorage.googleapis.com/v0/b/strange-reducer-431108-b9.appspot.com/o/dog.jpg?alt=media&token=04ecca87-b341-4352-a092-53fd2b967361',
        text='輸入以下指令來照顧小吉吧!',
        actions=[
            MessageAction(label='我要領養小吉', text='我要領養小吉'),
        ]
    )
    return TemplateSendMessage(alt_text='在路上遇到了一隻小吉!', template=buttons_template)

def instruction():
    buttons_template = ButtonsTemplate(
        title='開始照顧小吉!',
        thumbnail_image_url='https://firebasestorage.googleapis.com/v0/b/strange-reducer-431108-b9.appspot.com/o/dog.jpg?alt=media&token=04ecca87-b341-4352-a092-53fd2b967361',
        text='汪汪汪汪汪汪汪汪!!!',
        actions=[
            MessageAction(label='照顧小吉 記錄生活', text='呼叫小吉'),
            MessageAction(label='叫小吉幫忙整理櫃子', text='小吉幫忙'),
            MessageAction(label='再次放生小吉', text='放生小吉'),
            URIAction(label='一探究竟小吉的一生', uri='https://franchingkao.github.io/2024/08/21/chatbot-chiwa/'),
            # PostbackAction(label='點擊按鈕', data='button_clicked')
        ]
    )
    return TemplateSendMessage(alt_text='汪汪汪汪汪汪汪汪!!!', template=buttons_template)

def callChiwa():
    return TextSendMessage(
        text='汪叫我幹嘛?',
        quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(label='尿尿', text='小吉尿尿'),
                image_url='https://firebasestorage.googleapis.com/v0/b/strange-reducer-431108-b9.appspot.com/o/91516.png?alt=media&token=c311e922-0e73-4021-9deb-0582169ea265'
            ),
            QuickReplyButton(
                action=MessageAction(label='大便', text='小吉大便'),
                image_url='https://firebasestorage.googleapis.com/v0/b/strange-reducer-431108-b9.appspot.com/o/8211907.png?alt=media&token=eb6f79be-f491-4344-87f1-138e6ce58292'
            ),
            QuickReplyButton(
                action=MessageAction(label='喝水', text='小吉喝水'),
                image_url='https://cdn-icons-png.flaticon.com/128/6002/6002889.png'
            ),
            QuickReplyButton(
                action=MessageAction(label='散步', text='小吉跑跑'),
                image_url='https://cdn-icons-png.flaticon.com/128/6401/6401079.png'
            ),
            QuickReplyButton(
                action=MessageAction(label='摸摸', text='最近怎麼樣'),
                image_url='https://cdn-icons-png.flaticon.com/128/2138/2138440.png'
            ),
            ]
        )
    )

def helpChiwa():
    return TextSendMessage(
        text='汪叫我幹嘛?',
        quick_reply=QuickReply(
        items=[
            QuickReplyButton(
                action=MessageAction(label='翻翻零食櫃', text='小吉看看零食櫃'),
                # image_url='https://cdn-icons-png.flaticon.com/128/3629/3629576.png'
            ),
            QuickReplyButton(
                action=MessageAction(label='買零食', text='打開零食櫃'),
                # image_url='https://cdn-icons-png.flaticon.com/128/3629/3629576.png'
            ),
            QuickReplyButton(
                action=MessageAction(label='清空零食櫃', text='清空零食櫃'),
                # image_url='https://cdn-icons-png.flaticon.com/128/11427/11427614.png'
            ),
            QuickReplyButton(
                action=MessageAction(label='整理零食櫃', text='整理零食櫃'),
                # image_url='https://cdn-icons-png.flaticon.com/128/3063/3063644.png'
            ),
            QuickReplyButton(
                action=MessageAction(label='翻翻櫥櫃', text='小吉看看櫥櫃'),
                # image_url='https://cdn-icons-png.flaticon.com/128/3629/3629576.png'
            ),
            QuickReplyButton(
                action=MessageAction(label='買日用品', text='打開櫥櫃'),
                # image_url='https://cdn-icons-png.flaticon.com/128/3629/3629576.png'
            ),
            QuickReplyButton(
                action=MessageAction(label='清空櫥櫃', text='清空櫥櫃'),
                # image_url='https://cdn-icons-png.flaticon.com/128/11427/11427614.png'
            ),
            QuickReplyButton(
                action=MessageAction(label='整理櫥櫃', text='整理櫥櫃'),
                # image_url='https://cdn-icons-png.flaticon.com/128/3063/3063644.png'
            ),
            ]
        )
    )

def byeChiwa():
    confirm_template = ConfirmTemplate(
        text='放生小吉會遺失零食櫃、櫥櫃，還有與小吉的回憶，確定要放生小吉嗎?',
        actions=[
            MessageAction(label='放生牠', text='再見小吉'),
            MessageAction(label='撿回家', text='捨不得小吉')
        ])
    return TemplateSendMessage(alt_text='汪汪汪汪汪汪汪汪汪????', template=confirm_template)


def ifBlankStorage():
    buttons_template = ButtonsTemplate(
        title='櫃子空空的...',
        thumbnail_image_url='https://firebasestorage.googleapis.com/v0/b/strange-reducer-431108-b9.appspot.com/o/dog.jpg?alt=media&token=04ecca87-b341-4352-a092-53fd2b967361',
        text='放點東西進來吧!',
        actions=[
            MessageAction(label='打開零食櫃', text='打開零食櫃\n小吉飼料 1 2024/08/31\n小吉潔牙骨 2\n小吉餅乾'),
            MessageAction(label='打開櫥櫃', text='打開櫥櫃\n小吉尿布 1 2024/08/31\n小吉的床\n小吉的玩具 5'),
        ]
    )
    return TemplateSendMessage(alt_text='櫃子空空的...', template=buttons_template)

def ifBlankChiwa():
    buttons_template = ButtonsTemplate(
        title='最近都不愛我...',
        thumbnail_image_url='https://firebasestorage.googleapis.com/v0/b/strange-reducer-431108-b9.appspot.com/o/dog.jpg?alt=media&token=04ecca87-b341-4352-a092-53fd2b967361',
        text='快來寵小吉吧!帶小吉去...',
        actions=[
            MessageAction(label='尿尿', text='小吉尿尿'),
            MessageAction(label='大便', text='小吉大便'),
            MessageAction(label='散步', text='小吉跑跑'),
            MessageAction(label='喝水', text='小吉喝水'),
        ]
    )
    return TemplateSendMessage(alt_text='最近都不愛我...', template=buttons_template)

def addItem(msg):
    today = datetime.date.today()

    info = msg.strip().split(' ')
    if len(info) == 1:
        item = info[0]
        value = 1
        exp = today + datetime.timedelta(days=7)
    
    elif len(info) == 2:
        item = info[0]
        if '/' in info[1]:
            exp = parser.parse(info[1], fuzzy=True).date()
            value = 1
        else:
            value = info[1]
            exp = today + datetime.timedelta(days=7)

    elif len(info) == 3:
        item, value, exp = info
        exp = parser.parse(exp, fuzzy=True).date()
    
    return item, int(value), exp

def sortStorage(records):         
    with open(os.path.join('template', 'warehouse_s.json'), 'r') as file:
        flex = json.load(file)
    with open(os.path.join('template', 'warehouse_m.json'), 'r') as file:
        tmp = json.load(file)

    result = defaultdict(int)

    for entry in records:
        key = (entry['expiration'], entry['item'])
        result[key] += entry['value']

    for (expiration, item), value in sorted(result.items()):
        print(f"{expiration} {item} {value}")
        tmp['contents'][0]['text'] = f'{expiration}'
        tmp['contents'][1]['text'] = f'{item}'
        tmp['contents'][2]['text'] = f'{value}'
        
        flex['body']['contents'][3]['contents'].append(copy.deepcopy(tmp))
    
    return flex

def sortChiwa(records):
    with open(os.path.join('template', 'life_s.json'), 'r') as file:
        flex = json.load(file)
    with open(os.path.join('template', 'life_m.json'), 'r') as file:
        tmp = json.load(file)
        
    result = defaultdict(lambda: defaultdict(int))

    for entry in records:
        date = entry['datetime']
        item = entry['item']
        value = entry['value']
        result[date][item] += value

    items = ['喝水', '尿尿', '大便', '跑跑']
    for date in sorted(result.keys()):
        values = [date] + [str(result[date].get(item, 0)) for item in items]
        for i, data in enumerate(values):
            tmp['contents'][i]['text'] = f'{data}'
        flex['body']['contents'][2]['contents'].append(copy.deepcopy(tmp))

    return flex

def dropSth(msg, records):
    msg = msg.strip().split(' ')
    if len(msg) == 2:
        records = [record for record in records if (record['item'] != msg[0] or parser.parse(record['expiration'], fuzzy=True).date() != parser.parse(msg[1], fuzzy=True).date())]
    elif len(msg) == 1:
        records = [record for record in records if record['item'] != msg[0]]
    
    return records