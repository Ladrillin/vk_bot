import vk_api
import json
import networkx as nx
import matplotlib.pyplot as mpl


def auth_handler():
    code = input('Input auth code: ')
    remember_device = True
    return code, remember_device


def parsing_level_1(root_id, friends_list_id):
    mpl.rcParams.update({'font.size': 8})
    graph_network = nx.Graph()
    users_info_list_test = []
    """ for friend_id in friends_list_id['items']:
        user_info = vk.users.get(user_ids=friend_id,
                                 fields='bdate, connections')
        users_info_list_test.append(user_info) """
    graph_network.add_node(root_id)
    counter = 0
    for friend_id in friends_list_id['items']:  # Создаём первый уровень ака связи рут + все друзья
        graph_network.add_edge(root_id, friend_id)
    for root_mutual_friend_id in friends_list_id['items']:
        try:
            get_mutual = vk.friends.getMutual(source_uid=root_id,
                                              target_uid=root_mutual_friend_id)
            for mutual_friend in get_mutual:
                graph_network.add_edge(root_mutual_friend_id, mutual_friend)
                counter += 1
        except vk_api.exceptions.ApiError:
            continue
        """with open('friend_list.json', 'w', encoding='utf-8') as json_file:
        json.dump(users_info_list_test, json_file, indent=4, sort_keys=True)"""
    nx.draw(graph_network, with_labels=True)
    print(counter)
    return mpl.show()


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

source_id = 141311052
getting_friends = vk.friends.get(user_id=source_id,)
print(getting_friends)
parsing_level_1(source_id, getting_friends)
