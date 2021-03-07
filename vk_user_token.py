import vk_api
import json


def auth_handler():
    code = input('Input auth code: ')
    remember_device = True
    return code, remember_device


def parsing_level_1(friends_list_id):
    users_info_list_test = []
    for friend_id in friends_list_id['items']:
        user_info = vk.users.get(user_ids=friend_id,
                                 fields='bdate, connections')
        users_info_list_test.append(user_info)
    """with open('friend_list.json', 'w', encoding='utf-8') as json_file:
        json.dump(users_info_list_test, json_file, indent=4, sort_keys=True)"""


with open('access_to_vk.txt', 'r') as access_file:
    login = access_file.readline()
    password = access_file.readline()

vk_session = vk_api.VkApi(login=login,
                          password=password,
                          auth_handler=auth_handler)
try:
    vk_session.auth()
except vk_api.AuthError as error_msg:
    print(error_msg)
vk = vk_session.get_api()


getting_friends = vk.friends.get(user_id=153475582)  # friends.getMutual для closed профилей
print(getting_friends)                               # С target_uid И source_uid вместо user_id
# parsing_level_1(getting_friends)
