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
        print("Bot: " + (_respone[0]['text']))
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
