import requests
import vk_api
import s_logger as log
from vk_api.utils import get_random_id
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from cfg import TOKEN, GID

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
poll = VkBotLongPoll(vk_session, GID)


def main():
    log.log('LinkCut Vk Bot Started\n')
    try:
        for event in poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.message:
                if event.from_user and (event.message['text'] != '' or event.message['attachments'] != []):
                    uid = event.message['from_id']
                    umsg = str(event.message['text'])
                    if umsg == '':
                        at = event.message['attachments']
                        at = at[0]
                        # for link in at:
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
                        try:
                            response = requests.post('http://www.linkcut.ru', data=payload)
                            msg = response.text
                        except requests.exceptions.ConnectionError:
                            log.log('Connection Error')
                            msg = 'Временная ошибка сервера, попробуйте чуть позже'
                        except requests.exceptions.BaseHTTPError:
                            log.log('HTTP error')
                            msg = 'Временная ошибка сервера, попробуйте чуть позже'
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
    except vk_api.ApiError as err:
        log.log('Error occurs: ' + str(err.error))
    except vk_api.ApiHttpError as err:
        log.log('Error occurs: ' + str(err.values))
    except vk_api.VkRequestsPoolException as err:
        log.log('Error occurs: ' + str(err.error))
    except requests.exceptions.ReadTimeout as err:
        log.log('Error occurs: ' + str(err.error))


if __name__ == '__main__':
    main()
