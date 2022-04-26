import datetime
import pprint
import random

import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

TOKEN = "822b2ed110c687232450ea4d8d724cb2cf3efb246a4e259f1650c3f4ce9301cdbdf0cd2e8cfba0b817d90"


def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, 212918059)
    vk = vk_session.get_api()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and '!news' not in event.obj.message['text']\
                and '!users' not in event.obj.message['text']:
            user = vk.users.get(user_id=event.obj.message['from_id'])
            vk.messages.send(user=user[0]['id'], peer_id=user[0]['id'],
                             message=f'Здравствуйте, я бот сайта Aglomerat.\n'
                                     f'У меня можно получить информацию о пользователях'
                                     f' и новостях.\n'
                                     f'\n'
                                     f'Команды:\n'
                                     f'!news <id>\n'
                                     f'!users <id>',
                             random_id=random.randint(0, 10 ** 9))
        elif event.type == VkBotEventType.MESSAGE_NEW and '!news' in event.obj.message['text']:
            user = vk.users.get(user_id=event.obj.message['from_id'])
            single_post = False
            if event.obj.message['text'].rfind(' ') == -1:
                response = requests.get('http://127.0.0.1:8080/api/news')
            else:
                query = 'http://127.0.0.1:8080/api/news/' + \
                        event.obj.message['text'][event.obj.message['text'].rfind(' ') + 1:]
                response = requests.get(query)
                single_post = True

            if "error" in response.json().keys():
                pass

            item = response.json()["news"]
            pprint.pprint(item)
            vk.messages.send(user=user[0]['id'], peer_id=user[0]['id'],
                             message=f'NewsAPI:',
                             random_id=random.randint(0, 10 ** 9))
            if single_post:
                vk.messages.send(user=user[0]['id'], peer_id=user[0]['id'],
                                 message=f'Заголовок - {item["title"]}\n'
                                         f'Автор - {item["user"]["name"]}\n'
                                         f'Дата публикации - '
                                         f'{datetime.date.fromtimestamp(item["created_date"])}\n'
                                         f'Содержание:\n'
                                         f'{item["content"]}',
                                 random_id=random.randint(0, 10 ** 9))

        elif event.type == VkBotEventType.MESSAGE_NEW and '!users' in event.obj.message['text']:
            single_user = False
            user = vk.users.get(user_id=event.obj.message['from_id'])
            if event.obj.message['text'].rfind(' ') == -1:
                response = requests.get('http://127.0.0.1:8080/api/users')
            else:
                query = 'http://127.0.0.1:8080/api/users/' + \
                        event.obj.message['text'][event.obj.message['text'].rfind(' ') + 1:]
                response = requests.get(query)
                single_user = True
            item = response.json()["users"]
            pprint.pprint(item)
            vk.messages.send(user=user[0]['id'], peer_id=user[0]['id'],
                             message=f'UsersAPI:',
                             random_id=random.randint(0, 10 ** 9))
            if single_user:
                vk.messages.send(user=user[0]['id'], peer_id=user[0]['id'],
                                 message=f'ID - {item["id"]}\n'
                                         f'Имя пользователя - {item["name"]}\n'
                                         f'email - {item["email"]}\n'
                                         f'Дата регистрации - '
                                         f'{datetime.date.fromtimestamp(item["created_date"])}\n'
                                         f'Графа "о себе" - {item["about"]}\n',
                                 random_id=random.randint(0, 10 ** 9))
            else:
                vk.messages.send(user=user[0]['id'], peer_id=user[0]['id'],
                                 message=f'Количество пользователей: {len(item)}\n'
                                         f'Для информации по конкретному пользователю '
                                         f'используйте id',
                                 random_id=random.randint(0, 10 ** 9))


if __name__ == '__main__':
    main()
