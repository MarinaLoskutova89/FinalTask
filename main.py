import json
import YaDisk
import VKUser
from functools import cmp_to_key

with open('token_vk_user.txt', 'r', encoding='utf-8') as file_object:
    token = file_object.read().strip()

with open('token_yandex.txt', 'r', encoding='utf-8') as file_object:
    token_yandex = file_object.read().strip()

vk_client = VKUser.VKUser(token, '5.131')
data = vk_client.get_photos('552934290', 'profile')
y = YaDisk.YandexDisk(token=token_yandex)

def compare(item1, item2):

    d = {'s': 0, 'm': 1, 'x': 2, 'o': 3, 'p': 4, 'q': 5, 'r': 6, 'y': 7, 'z': 8, 'w': 9}

    if item1['width'] * item1['height'] == item2['width'] * item2['height'] and d[item1['type']] > d[item2['type']]:
        return 1
    elif item1['width'] * item1['height'] == item2['width'] * item2['height'] and d[item1['type']] < d[item2['type']]:
        return -1
    else:
        return 0

photo_list = []
for item in data['response']['items']:
    photo_list.append({'likes': item['likes']['count'],
                       'date': item['date'],
                       'url': item['sizes']})
sorted_photo_list = sorted(photo_list, key=lambda x: x['likes'])
photo = {}
photo_info = []
for file_name in photo_list:
    max_photo = sorted(file_name['url'], key=lambda x: x['width'] * x['height'], reverse=True)
    max_photo_sorted = sorted(max_photo, key=cmp_to_key(compare), reverse=True)
    items = max_photo_sorted[0]
    like = file_name['likes']
    name = f'{like}.jpg'
    url = items['url']
    size = items['type']
    if name not in photo.keys():
        photo[name] = url
    else:
        another_name = str(like) + '_' + str(file_name['date'])
        name = f'{another_name}.jpg'
        photo[name] = url
    photo_info.append({'file name': name, 'size': size})
    with open('photo_info.json', 'w', encoding='utf-8') as file:
        json.dump(photo_info, file, indent=2, ensure_ascii=False)

y.upload_files_to_disk('/Photo from VK', photo)