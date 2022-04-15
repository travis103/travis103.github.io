import json
import time

import requests
import subprocess

URL = "https://api.telegram.org/bot{}/".format("1170736461:AAEIuckUxB5Vp5T_GsN7OfxEbvtqZI-tqws")

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js


def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]

    chat_id = updates["result"][last_update]["message"]["chat"]["id"]

    if (text, chat_id) != last_textchat and text[0]=='T' :
        textx=text.split(' ')
        send_message("Message frequency changed to "+textx[1]+ " seconds." , chat_id)
        global messageFreq
        messageFreq=int(textx[1])

    elif (text, chat_id) != last_textchat and text[0]=="hi":
        send_message("%s" % "hello" , chat_id)

    elif (text, chat_id) != last_textchat:
        # subprocess.call('%s' % text, shell=True)
        proc = subprocess.Popen('%s' % text, shell=True, stdout=subprocess.PIPE)
        output = proc.stdout.read()
        send_message("%s finished" % text , chat_id)
        send_message("result is %s" % output, chat_id)

    return (text, chat_id)



def main():
    global last_textchat
    last_textchat = (None, None)
    global messageFreq
    messageFreq=30 #inSeconds

    while True:
        text, chat = get_last_chat_id_and_text(get_updates())
        if (text, chat) != last_textchat:
            last_textchat = (text, chat)
        time.sleep(messageFreq)


if __name__ == '__main__':
    main()
