import requests
import json


def send_message(id_sender, message):
    # call api url
    url = "http://127.0.0.1:5005/webhooks/rest/webhook"
    # data
    data_dict = {"sender": id_sender, "message": message}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # jsonify data to send
    data = json.dumps(data_dict)
    # read respone text
    try:
        _request = requests.post(url, data, headers)
        _respone = json.loads(_request.text)
        reply_url = ''
        # Dịch vụ FiberVNN
        if ('#fiber' in _respone_bot[0]['text']):
            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + sender_id + '&ma_dichvu=fiber'
            print(_respone_bot[0]['text'].replace('#fiber', reply_url))
        # Dịch vụ MyTV
        elif ('#mytv' in _respone_bot[0]['text']):
            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + sender_id + '&ma_dichvu=mytv'
            print(_respone_bot[0]['text'].replace('#mytv', reply_url))
        # Dịch vụ di động
        elif ('#didong' in _respone_bot[0]['text']):
            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + sender_id + '&ma_dichvu=didong'
            print(_respone_bot[0]['text'].replace('#didong', reply_url))
        # Dịch vụ chữ ký số
        elif ('#chukyso' in _respone_bot[0]['text']):
            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + sender_id + '&ma_dichvu=chukyso'
            print(_respone_bot[0]['text'].replace('#chukyso', reply_url))
        # Dịch vụ hóa đơn điện tử
        elif ('#hddt' in _respone_bot[0]['text']):
            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + sender_id + '&ma_dichvu=hddt'
            print(_respone_bot[0]['text'].replace('#hddt', reply_url))
        # Dịch vụ pharmacy
        elif ('#pharmacy' in _respone_bot[0]['text']):
            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + sender_id + '&ma_dichvu=pharmacy'
            print(_respone_bot[0]['text'].replace('#pharmacy', reply_url))
        # Dịch vụ Bảo hiểm xã hội
        elif ('#bhxh' in _respone_bot[0]['text']):
            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + sender_id + '&ma_dichvu=bhxh'
            print(_respone_bot[0]['text'].replace('#bhxh', reply_url))
        # Dịch vụ khác
        elif ('#khac' in _respone_bot[0]['text']):
            reply_url = 'https://vnptvinhlong.vn/donhang/tao?zaloid=' + sender_id + '&ma_dichvu=khac'
            print(_respone_bot[0]['text'].replace('#khac', reply_url))
    except:
        print("Connection Error!")


# Main func
if __name__ == "__main__":
    sender_id = str(input("Type your ID: "))
    print("(-stop if want to stop)")
    while True:
        message = str(input(sender_id + ": "))
        if message == "-stop":
            break
        else:
            send_message(sender_id, message)
