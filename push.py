import os
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage, FlexSendMessage
from firebase import firebase
from utils import *

channel_access = os.environ.get('CHANNEL_ACCESS_TOKEN')
firebase_url = os.getenv('FIREBASE_URL')

def get_data(fdb, path):
    return [] if fdb.get(path, None) is None else fdb.get(path, None)

def pushmsg(request):    
    line_bot_api = LineBotApi(channel_access)
    fdb = firebase.FirebaseApplication(f'{firebase_url}', None)
    users = fdb.get(f'{firebase_url}/chat', None)
    user_ids = [user_id for user_id in users if len(user_id)>30]
    
    for user_id in user_ids:
        snack_path = f'chat/{user_id}/snack'
        records = get_data(fdb, snack_path)
        flex = sortStorage(records)
        flex_msg = FlexSendMessage(alt_text='小吉來了', contents=flex)
        line_bot_api.push_message(user_id, flex_msg)
    return 'ok'