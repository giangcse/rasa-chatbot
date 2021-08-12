from fastapi import FastAPI, Form
# from pydantic import BaseModel

import json
import requests

app = FastAPI()

# class message(BaseModel):
#     user_id: str = "1"
#     user_msg: str = ""


@app.post("/")
async def index(user_id: str = Form(...), user_msg: str = Form(...)):
    # user_id = request.form.get('user_id')
    # user_msg = request.form.get('user_msg')
    if user_id is not None:
        # call api url
        url = "http://127.0.0.1:5005/webhooks/rest/webhook"
        # data
        data_dict = {"sender": user_id, "message": user_msg}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # jsonify data to send
        data = json.dumps(data_dict)
        # read respone text
        try:
            _request = requests.post(url, data, headers)
            _respone = json.loads(_request.text)
            reply_url = ''
            finally_respone = ''
            # Dịch vụ FiberVNN
            if ('#fiber' in _respone[0]['text']):
                reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                    user_id + '&ma_dichvu=fiber'
                finally_respone = _respone[0]['text'].replace(
                    '#fiber', reply_url)
            # Dịch vụ MyTV
            elif ('#mytv' in _respone[0]['text']):
                reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                    user_id + '&ma_dichvu=mytv'
                finally_respone = _respone[0]['text'].replace(
                    '#mytv', reply_url)
            # Dịch vụ di động
            elif ('#didong' in _respone[0]['text']):
                reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                    user_id + '&ma_dichvu=didong'
                finally_respone = _respone[0]['text'].replace(
                    '#didong', reply_url)
            # Dịch vụ chữ ký số
            elif ('#chukyso' in _respone[0]['text']):
                reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                    user_id + '&ma_dichvu=chukyso'
                finally_respone = _respone[0]['text'].replace(
                    '#chukyso', reply_url)
            # Dịch vụ hóa đơn điện tử
            elif ('#hddt' in _respone[0]['text']):
                reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                    user_id + '&ma_dichvu=hddt'
                finally_respone = _respone[0]['text'].replace(
                    '#hddt', reply_url)
            # Dịch vụ pharmacy
            elif ('#pharmacy' in _respone[0]['text']):
                reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                    user_id + '&ma_dichvu=pharmacy'
                finally_respone = _respone[0]['text'].replace(
                    '#pharmacy', reply_url)
            # Dịch vụ Bảo hiểm xã hội
            elif ('#bhxh' in _respone[0]['text']):
                reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                    user_id + '&ma_dichvu=bhxh'
                finally_respone = _respone[0]['text'].replace(
                    '#bhxh', reply_url)
            # Dịch vụ khác
            elif ('#khac' in _respone[0]['text']):
                reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                    user_id + '&ma_dichvu=khac'
                finally_respone = _respone[0]['text'].replace(
                    '#khac', reply_url)
            else:
                finally_respone = _respone[0]['text']

            return json.loads(json.dumps({'status': 'success', 'message': finally_respone}))
        except ConnectionError:
            return json.loads(json.dumps({'status': 'error', 'message': 'ConnectionError'}))
