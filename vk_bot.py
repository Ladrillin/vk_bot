import vk_api
import weather_module
import random
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

vk = vk_api.VkApi(token='',
                  api_version='5.130')
vk_session_test = vk.get_api()
longpoll = VkLongPoll(vk)


def keyboard_func():
    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Зелёная кнопка', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Красная кнопка', color=VkKeyboardColor.NEGATIVE)

    keyboard.add_line()
    keyboard.add_location_button()

    vk_session_test.messages.send(
        peer_id=141498951,
        random_id=random.randint(100000, 1000000),
        keyboard=keyboard.get_keyboard(),
        message='Пример клавиатуры'
    )


def message_recognition(message_text):
    hello_set = ('привет', 'hi', 'hello')
    if message_text in hello_set:
        write_msg(event.user_id, 'Hello there, mate')
        keyboard_func()
    if message_text.startswith('погода') or \
       message_text.startswith('weather'):
        ya_weather(event.user_id, str(query_text[7:]))
    if query_text.startswith('id'):
        try:
            user_info_func(str(query_text[2:]), event.user_id)
        except KeyError:
            write_msg(event.user_id, 'Кажется юзера с таким id не существует.')


def user_info_func(uid, recipient_id):  # uid - id человека, по которому пробивается инфа
    info = vk.method('users.get', {'user_ids': uid,
                                   'fields': 'city, connections, relation, bdate, last_seen(time), has_mobile'
                                             'contancts, relatives'
                                             'home_town, sex, deactivated, personal, timezone, followers_count'})
    write_msg(recipient_id, str(info))
    print(info)


def ya_weather(user_id, city_name):
    full_data = weather_module.yandex_weather(city_name)  # Респонс от апи Я.Погоды
    formatted_data = weather_module.weather_formatting(full_data)  # Взятие нужных данных из full_data
    answer = weather_module.weather_info_text(formatted_data)  # Формирование текстового ответа из данных
    write_msg(user_id, answer)


def write_msg(user_id, message):
    random_id = event.random_id
    vk.method('messages.send', {'user_id': user_id,
                                'message': message,
                                'random_id': random_id})


def write_msg_photo(user_id, message, attachment):  # Вк.метод отправки сообщения
    random_id = event.random_id
    vk.method('messages.send', {'user_id': user_id,
                                'message': message,
                                'random_id': random_id,
                                'attachment': ','.join(attachment)})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        query_text = event.text
        query_attachment = event.attachments
        getting_info = vk.method('messages.getById', {'group_id': 197844560,  # Массив. Информация о сообщении
                                                      'message_ids': event.message_id})
        message_recognition(query_text)  # Работа с текстовым сообщением
        if query_attachment:  # Работа с ответной пикчей
            print(query_attachment)
            try:
                returned_attachments_list = []
                attachment_list = getting_info['items'][0]['attachments']
                for each_attachment in attachment_list:
                    step_attachment = each_attachment['photo']
                    one_of_the_attachments = "photo{}_{}_{}".format(step_attachment['owner_id'],
                                                                    step_attachment['id'],
                                                                    step_attachment['access_key'])
                    returned_attachments_list.append(one_of_the_attachments)
                if len(query_attachment) == 2:
                    write_msg_photo(event.user_id, 'Nice pic, bro.', returned_attachments_list)
                else:
                    write_msg_photo(event.user_id, 'Awesome photos, man.', returned_attachments_list)
            except KeyError:
                write_msg(event.user_id, 'Кажется это была не фотография.')
