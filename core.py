import requests
import vk_api
import logging as log
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from cfg import TOKEN, GID

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
poll = VkBotLongPoll(vk_session, GID)


def main():
    log.log('LinkCut Vk Bot Started')
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

                log.log('UID: ' + str(uid) + '\tMSG: ' + umsg + '\tRequest: ' + msg)
                vk.messages.send(
                    random_id=get_random_id(),
                    message=msg,
                    user_id=uid
                )
            if event.from_chat:
                log.log('its chat')
            if event.from_group:
                log.log('its group')


if __name__ == '__main__':
    main()
