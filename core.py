import requests
from datetime import datetime
import vk_api
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from cfg import TOKEN, GID

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
poll = VkBotLongPoll(vk_session, GID)


def log(info):
    info = '\n' + str(datetime.now()) + '\t' + info + '\n'
    print(info)
    with open('logs.txt', 'a') as logFile:
        logFile.write(info)


def main():
    log('LinkCut Vk Bot Started')
    for event in poll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.message:
            if event.from_user and (event.message['text'] != '' or event.message['attachments'] != []):
                uid = event.message['from_id']
                umsg = str(event.message['text'])
                if umsg == '':
                    at = event.message['attachments']
                    at = at[0]
                    #for link in at:
                    if at['type'] == 'link':
                        link = at['link']
                        umsg = link['url']
                    else:
                        umsg = 'Ошибка'
                if umsg.lower() == 'начать':
                    msg = 'Добро пожаловать! Для сокращения ссылки просто напишите ее сюда :)'
                elif umsg.lower() == 'ошибка':
                    msg = 'Произошла оказия, попробуйте еще раз'
                else:
                    payload = {'link_in': umsg, 'userType': 'vkBot'}
                    response = requests.post('http://www.linkcut.ru', data=payload)
                    msg = response.text
                    if response.status_code in (500, 404, 400):
                        msg = 'Ошибка сервера :('

                log('\nUID: ' + str(uid) + '\tMSG: ' + umsg + '\tRequest: ' + msg)
                vk.messages.send(
                    random_id=get_random_id(),
                    message=msg,
                    user_id=uid
                )
            if event.from_chat:
                log('its chat')
            if event.from_group:
                log('its group')


if __name__ == '__main__':
    main()
