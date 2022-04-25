import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

TOKEN = "822b2ed110c687232450ea4d8d724cb2cf3efb246a4e259f1650c3f4ce9301cdbdf0cd2e8cfba0b817d90"


def main():
    vk_session = vk_api.VkApi(token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, 212918059)
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            user = vk.users.get(user_id=event.obj.message['from_id'])
            vk.messages.send(user=event.obj.message['from_id'],
                             message=f'Здравствуйте, я бот сайта Aglomerat.'
                                     f'')
            print(user)


if __name__ == '__main__':
    main()
