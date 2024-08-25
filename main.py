# https://medium.com/@pearl3904/linebot%E5%AF%A6%E4%BD%9C-%E6%A9%9F%E5%99%A8%E4%BA%BA%E5%82%B3%E9%80%81%E7%9A%84%E8%A8%8A%E6%81%AF%E7%A8%AE%E9%A1%9E%E5%A4%A7%E5%BD%99%E6%95%B4-89201c2167fd#0dee
# https://ithelp.ithome.com.tw/articles/10285407
# https://steam.oxxostudio.tw/category/python/example/line-flex-message.html

import os
import json
import pandas as pd
import hmac
import hashlib
import base64
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage, ConfirmTemplate, MessageAction, TemplateSendMessage, QuickReply, QuickReplyButton, ButtonsTemplate, URIAction
from linebot.models import TextSendMessage, FlexSendMessage
from firebase import firebase
import datetime
from dateutil import parser
from utils import *
import copy
from collections import defaultdict

channel_access = os.environ.get('CHANNEL_ACCESS_TOKEN')
channel_secret = os.environ.get('CHANNEL_SECRET_TOKEN')
firebase_url = os.getenv('FIREBASE_URL')

def get_data(fdb, path):
    return [] if fdb.get(path, None) is None else fdb.get(path, None)

def linebot(request):
    today = datetime.date.today()

    if request.method == 'POST':
        if 'X-Line-Signature' not in request.headers:
            return 'Error: Invalid source', 403
        else:
            x_line_signature = request.headers['X-Line-Signature']
            line_bot_api = LineBotApi(channel_access)
            handler = WebhookHandler(channel_secret)

            body = request.get_data(as_text=True)
            json_data = json.loads(body)

            hash = hmac.new(channel_secret.encode('utf-8'),
                        body.encode('utf-8'), hashlib.sha256).digest()
            signature = base64.b64encode(hash).decode('utf-8')

            if x_line_signature == signature:
                ###########################
                # ====== settings ======= # 
                ###########################
                # load message from the user
                handler.handle(body, x_line_signature)
                event = json_data['events'][0]
                tk = event['replyToken']
                msg = event['message']['text']
                msgs = msg.split('\n') if '\n' in msg else [msg]
                user_id = event['source']['userId']

                # connect to database
                fdb = firebase.FirebaseApplication(firebase_url, None)
                user_chat_path = f'chat/{user_id}'
                snack_path = f'chat/{user_id}/snack'
                warehouse_path = f'chat/{user_id}/warehouse'
                life_path = f'chat/{user_id}/life'

                # obtain the existing contents in db
                messages = get_data(fdb, user_chat_path)
                life = get_data(fdb, life_path)
                
                ###########################
                # ====== functions ====== # 
                ###########################
                if msg == '小吉?':
                    reply_msg = firstMeet()
                
                elif msg == '我要領養小吉' or msg == '怎麼照顧小吉':
                    reply_msg = instruction()

                elif msg == '呼叫小吉' or msg == '小吉':
                    reply_msg = callChiwa()
                
                elif msg == '小吉幫忙':
                    reply_msg = helpChiwa()
                
                elif '小吉看看' in msg:
                    # today = pd.to_datetime('today').normalize()

                    records = fdb.get(warehouse_path, None) if '櫥櫃' in msg else fdb.get(snack_path, None)
                    
                    if records is None:
                        reply_msg = ifBlankStorage()
                    else:
                        flex = sortStorage(records)                     
                        reply_msg = FlexSendMessage(alt_text='小吉幫你整理好了', contents=flex)

                elif msg[:2] == '小吉':
                    life.append({'datetime': today, 'item': msg[2:], 'value':  1})
                    fdb.put_async(life_path, None, life)
                    reply_msg = TextSendMessage(text=f'汪汪!')
                
                elif '最近怎麼樣' in msg or '摸摸' in msg:
                    # today = pd.to_datetime('today').normalize()

                    records = fdb.get(life_path, None)

                    if records is None:
                        reply_msg = ifBlankChiwa()
                    else:
                        flex = sortChiwa(records)
                        reply_msg = FlexSendMessage(alt_text='汪汪!', contents=flex)
                                
                elif '放生小吉' in msg:
                    reply_msg = byeChiwa()

                elif msg == '再見小吉': 
                    fdb.put_async(user_chat_path, None , [{'init': 0}])
                    reply_msg = TextSendMessage(text=f'我是流浪小吉汪汪嗚')

                elif msg == '捨不得小吉':
                    reply_msg = TextSendMessage(text=f'小吉還是會永遠愛你<3')

                elif msg == '試試看吧小吉':
                    with open('flex.json', 'r') as file:
                        flex = json.load(file)
                    with open('flex_tmp.json', 'r') as file:
                        tmp = json.load(file)

                    tmp['contents'][0]['text'] = '2024/09/31'
                    tmp['contents'][1]['text'] = '小吉的飼料'
                    tmp['contents'][2]['text'] = '1'

                    flex['body']['contents'][2]['contents'].append(tmp)
                    
                    reply_msg = FlexSendMessage(alt_text='hello', contents=flex)
                
                elif '零食櫃' in msg or '櫥櫃' in msg:
                    save_dir = warehouse_path if '櫥櫃' in msgs[0] else snack_path
                    records = get_data(fdb, save_dir)
                    reply_msg = []

                    if '清空' in msgs[0]:
                        fdb.delete_async(save_dir, None)
                        reply_msg = TextSendMessage(text=f'好了! 全部都丟掉了!')
                        line_bot_api.reply_message(tk, reply_msg)
                        return 'OK', 200
                         
                    # add items to the list
                    elif '打開' in msgs[0]:
                        if len(msgs) == 1:
                            reply_msg = ifBlankStorage()
                            line_bot_api.reply_message(tk, reply_msg)
                            return 'OK', 200
                        else:
                            for msg in msgs[1:]:
                                item, value, exp = addItem(msg)               
                                records.append({'datetime': today, 'item': item, 'value':  value, 'expiration': exp})
                            fdb.put_async(save_dir, None, records)

                    # remove items from the list
                    elif '整理' in msgs[0]:
                        if len(msgs) == 1:
                            records = [record for record in records if parser.parse(record['expiration'], fuzzy=True).date() >= today]
                        else:
                           for msg in msgs[1:]:
                                records = dropSth(msg, records)
                        fdb.put_async(save_dir, None, records)

                    flex = sortStorage(records)                     
                    flex_msg = FlexSendMessage(alt_text='小吉幫你整理好了', contents=flex)
                    text_msg = TextSendMessage(text=f'好了! 小吉幫你整理好了!')
                    reply_msg = [flex_msg, text_msg]

                line_bot_api.reply_message(tk, reply_msg)
                return 'OK', 200

            else:
                return 'Invalid signature', 403
    else:
        return 'Method not allowed', 400