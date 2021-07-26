#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import pymongo


class Zalo():
    db_url = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    db_zalo = db_url["Zalo"]

    # Lay danh sach ID nhung nguoi dung quan tam ZOA
    def get_list_users_id(self, token):
        data = {"offset": 0, "count": 5}
        data = json.dumps(data)
        url = "https://openapi.zalo.me/v2.0/oa/getfollowers?data=" + \
            data + "&access_token=" + token

        try:
            _r = requests.get(url)
            respone = json.loads(_r.text)
            list_users = []
            for i in respone['data']['followers']:
                list_users.append(i['user_id'])

            return list_users
        except ConnectionError:
            print("Connection Error!")

    # Kiem tra xem user da co trong database chua
    def check_user_exists(self, user_id):
        zoa_users = self.db_zalo['zoa_users']
        try:
            count = zoa_users.count_documents({"user_id": user_id})
            if count == 0:
                return False
            else:
                return True
        except ConnectionError:
            print("Database Error!")

    # Lay thong tin tung nguoi dung quan tam ZOA
    def get_user_info(self, token):
        zoa_users = self.db_zalo['zoa_users']
        try:
            list_users = self.get_list_users_id(token)
            for i in list_users:
                data = json.dumps({"user_id": i})
                url = "https://openapi.zalo.me/v2.0/oa/getprofile?data=" + \
                    data + "&access_token=" + token
                try:
                    _r = requests.get(url)
                    respone = json.loads(_r.text)
                    user_data = {"user_id": respone['data']['user_id'], "user_name": respone['data']
                                 ['display_name'], "user_gender": respone['data']['user_gender']}
                    try:
                        if not self.check_user_exists(respone['data']['user_id']):
                            zoa_users.insert_one(user_data)
                            print(
                                "User", respone['data']['display_name'], "has been added to database.")
                        else:
                            print("User", respone['data']
                                  ['display_name'], "exists!")
                    except ConnectionError:
                        print("Database Error!")
                except ConnectionError:
                    print("Connection Error!")
        except ConnectionError:
            print("Connection Error!")

    # Kiem tra tin nhan da ton tai trong database chua
    def check_message_exist(self, message_id):
        zoa_messages = self.db_zalo['zoa_messages']
        count = zoa_messages.count_documents({"message_id": message_id})
        if count > 0:
            return True
        else:
            return False

    # Luu tin nhan nguoi dung
    def save_messages(self, token):
        zoa_messages = self.db_zalo['zoa_messages']
        zoa_users = self.db_zalo['zoa_users']
        offset = 0
        count = 10
        for i in zoa_users.find({}, {"user_id": 1}):
            user_id = int(i['user_id'])
            data = {"offset": offset, "user_id": user_id, "count": count}
            url = "https://openapi.zalo.me/v2.0/oa/conversation?data=" + \
                json.dumps(data) + "&access_token=" + token
            try:
                _r = requests.get(url)
                respone = json.loads(_r.text)
                conversation = respone['data']
                for j in conversation:
                    if self.check_message_exist(j['message_id']):
                        print("Message exists in database!")
                    else:
                        zoa_messages.insert_one(j)
                        print("Message", j['message_id'],
                              'has been added to database.')
            except ConnectionError:
                print("API Connection Error!")

    # Kiem tra tin nhan tu tung user xem da tra loi hay chua

    # Gui tin nhan den user
    def send_text_message(self, token, user_id, message):
        url = "https://openapi.zalo.me/v2.0/oa/message?access_token=" + token
        data = {"recipient": {"user_id": user_id},
                "message": {"text": message}}
        data = json.dumps(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        try:
            _r = requests.post(url, data, headers)
        except ConnectionError:
            print("Connection error!")

    # Bot tra loi qua zalo
    def bot_reply(self, token):
        replied_msg = self.db_zalo['replied_msg']
        url_zalo = "https://openapi.zalo.me/v2.0/oa/listrecentchat?data=%7B%22offset%22%3A0%2C%22count%22%3A10%7D&access_token=" + token
        try:
            _r_zalo = requests.get(url_zalo)
            data_zalo = json.loads(_r_zalo.text)
            lastest_message = data_zalo['data'][0]
            # print(lastest_message)
            if replied_msg.count_documents({"message_id": lastest_message['message_id']}) == 0:
                if lastest_message['src'] == 1 and lastest_message['type'] == "text":
                    url = "http://127.0.0.1:5005/webhooks/rest/webhook"
                    data_dict = {
                        "sender": lastest_message['from_display_name'], "message": lastest_message['message']}
                    data = json.dumps(data_dict)
                    headers = {'Content-type': 'application/json',
                               'Accept': 'text/plain'}
                    try:
                        _r_bot = requests.post(url, data, headers)
                        _respone_bot = json.loads(_r_bot.text)
                        # Tìm từ khóa trong câu trả lời của bot để đưa link vào
                        reply_url = ''
                        # Dịch vụ FiberVNN
                        if ('#fiber' in _respone_bot[0]['text']):
                            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                                lastest_message['from_id'] + '&ma_dichvu=fiber'
                            _respone_bot[0]['text'] = _respone_bot[0]['text'].replace(
                                '#fiber', reply_url)
                        # Dịch vụ MyTV
                        elif ('#mytv' in _respone_bot[0]['text']):
                            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                                lastest_message['from_id'] + '&ma_dichvu=mytv'
                            _respone_bot[0]['text'] = _respone_bot[0]['text'].replace(
                                '#mytv', reply_url)
                        # Dịch vụ di động
                        elif ('#didong' in _respone_bot[0]['text']):
                            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                                lastest_message['from_id'] + \
                                '&ma_dichvu=didong'
                            _respone_bot[0]['text'] = _respone_bot[0]['text'].replace(
                                '#didong', reply_url)
                        # Dịch vụ chữ ký số
                        elif ('#chukyso' in _respone_bot[0]['text']):
                            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                                lastest_message['from_id'] + \
                                '&ma_dichvu=chukyso'
                            _respone_bot[0]['text'] = _respone_bot[0]['text'].replace(
                                '#chukyso', reply_url)
                        # Dịch vụ hóa đơn điện tử
                        elif ('#hddt' in _respone_bot[0]['text']):
                            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                                lastest_message['from_id'] + '&ma_dichvu=hddt'
                            _respone_bot[0]['text'] = _respone_bot[0]['text'].replace(
                                '#hddt', reply_url)
                        # Dịch vụ pharmacy
                        elif ('#pharmacy' in _respone_bot[0]['text']):
                            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                                lastest_message['from_id'] + \
                                '&ma_dichvu=pharmacy'
                            _respone_bot[0]['text'] = _respone_bot[0]['text'].replace(
                                '#pharmacy', reply_url)
                        # Dịch vụ Bảo hiểm xã hội
                        elif ('#bhxh' in _respone_bot[0]['text']):
                            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                                lastest_message['from_id'] + '&ma_dichvu=bhxh'
                            _respone_bot[0]['text'] = _respone_bot[0]['text'].replace(
                                '#bhxh', reply_url)
                        # Dịch vụ khác
                        elif ('#khac' in _respone_bot[0]['text']):
                            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + \
                                lastest_message['from_id'] + '&ma_dichvu=khac'
                            _respone_bot[0]['text'] = _respone_bot[0]['text'].replace(
                                '#khac', reply_url)

                        self.send_text_message(
                            token, lastest_message['from_id'], _respone_bot[0]['text'])
                        replied_msg.insert_one(
                            {"message_id": lastest_message['message_id']})
                    except ConnectionError:
                        print("Cannot connect to bot")

        except ConnectionError:
            print("API Connection error!")

    # Lay anh ngau nhien tu database
    def random_image(self):
        import random
        img_db = self.db_zalo['zoa_images']
        max_id = img_db.count_documents({})
        rand_id = random.randint(0, int(max_id))
        return img_db.find_one({"id": rand_id})['url']

    # Gui tin nhan anh
    def send_image(self, token, user_id):
        img_url = self.random_image()
        url = "https://openapi.zalo.me/v2.0/oa/message?access_token=" + token
        header = {'Content-Type': 'application/json'}
        data = {
            "recipient": {
                "user_id": user_id
            },
            "message": {
                "text": "/-heart",
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "media",
                        "elements": [{
                            "media_type": "image",
                            "url": img_url
                        }]
                    }
                }
            }
        }
        try:
            _r = requests.post(url, json.dumps(data), header)
        except ConnectionError:
            print("Connection Error!")


if __name__ == "__main__":
    token = str("dGDnKxTiWacN0d5Rl6g6JPO3Sr-vSSiexabfJgHTq5ZsRcOPWctVRRTVI3YORiTVzsreBBzWssB2K3TviaQ2RTalCWY0Hv5_u7Pd9PHIaaZuI3qraK6EKSemEoAw5ezBbHuwFiS1f7Qd3bnvwGlVCwjkPsZALSepwcjWGA0QsGpG7653dGl69DyMCsFq6i4ctIDgSgWUuIR-TqvGe6EvF-v934kdPxWcx48tOSDRWWAhSYLeXqsTPzvJAngrIDX_mNzoA-jdqM_BUbjuiaNx4lLqULZQMiqWTHXSmIAsSO57")
    zalo = Zalo()
    while True:
        zalo.bot_reply(token)
