import json
import YaDisk
import VKUser

with open('token_vk_user.txt', 'r', encoding='utf-8') as file_object:
    token = file_object.read().strip()

with open('token_yandex.txt', 'r', encoding='utf-8') as file_object:
    token_yandex = file_object.read().strip()

vk_client = VKUser.VKUser(token, '5.131')
data = vk_client.get_photos('552934290', 'profile')
y = YaDisk.YandexDisk(token=token_yandex)

def get_largest_photo(size_dict):
    if size_dict['width'] >= size_dict['height']:
        return size_dict['width']
    else:
        return size_dict['height']

list = []
for item in data['response']['items']:
    list.append({'likes': item['likes']['count'], 'date': item['date'],
                 'url': item['sizes']})
sorted_list = sorted(list, key=lambda x: x['likes'])
photo = {}
photo_info = []
for file_name in list:
    like = file_name['likes']
    name = f'{like}.jpg'
    url = max(file_name['url'], key=get_largest_photo)['url']
    size = max(file_name['url'], key=get_largest_photo)['type']
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