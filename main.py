import requests
import json
import os
import yadisk
from dataclasses import dataclass
from pprint import pprint
# @dataclass
# class VKPic:
#     id: str
#     size: int
#     url: str
#     likes: int

with open('token_vk_user.txt', 'r', encoding='utf-8') as file_object:
    token = file_object.read().strip()

with open('token_yandex.txt', 'r', encoding='utf-8') as file_object:
    token_yandex = file_object.read().strip()

class VKUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version):
        self.params = {
            'access_token': token,
            'v': version
        }

    def write_json(self, data):
        with open('response.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def get_photos(self, owner_id, album_id):
        all_photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'extended': 1,
            'photo_sizes': 1
        }
        res = requests.get(all_photos_url, params={**self.params, **photos_params}).json()
        self.write_json(res['response']['items'])
        return res

    def get_largest_photo(self, size_dict):
        if size_dict['width'] >= size_dict['height']:
            return size_dict['width']
        else:
            return size_dict['height']

    # def largest_photo(self, file):
    #     url = []
    #     type = []
    #     photos = json.load(open(file))
    #     for photo in photos:
    #         sizes = photo['sizes']
    #         max_photos_url = max(sizes, key=self.get_largest_photo)['url']
    #         max_photos_size = max(sizes, key=self.get_largest_photo)['type']
    #         url.append(max_photos_url)
    #         type.append(max_photos_size)
    #         max_p = dict(zip(url, type))
    #     return url

    def make_direct(self, direct):
        if not os.path.isdir(direct):
            os.mkdir(direct)

    def download_photo(self, url, filename, direct):
        photo_url = url
        photo_name = filename
        photo = dict(zip(photo_url, photo_name))
        self.make_direct(direct)
        for key, value in photo.items():
            res = requests.get(key, stream=True)
            with open(f'{direct}/{value}.jpg', 'wb') as file:
                for chunk in res.iter_content(4096):
                    file.write(chunk)


vk_client = VKUser(token, '5.131')
data = vk_client.get_photos('552934290', 'profile')

list = []
for item in data['response']['items']:
    list.append({'likes': item['likes']['count'], 'date': item['date'],
                 'url': item['sizes']})
sorted_list = sorted(list, key=lambda x: x['likes'])
p = {}
for file_name in list:
    like = file_name['likes']
    url = max(file_name['url'], key=vk_client.get_largest_photo)['url']
    size = max(file_name['url'], key=vk_client.get_largest_photo)['type']
    if file_name['likes'] not in p.keys():
        name = f'{like}.jpg'
        p[name] = url
    else:
        another_name = str(like) + str(file_name['date'])
        name = f'{another_name}.jpg'
        p[name] = url

pprint(p)


# print(file_name)

# vk_client.download_photo(url, filename, 'Photo')


# list = []
# for item in data['response']['items']:
#     for size in item['sizes']:
#         ss = size['width'] * size['height']
#         pic = VKPic(item['id'], ss, size['url'], item['likes']['count'])
#         # pic = [item['id'], ss, size['url'], item['likes']['count']]
#         list.append(pic)
#         itema = [d for d in list if d.size == max(d.size for d in list)]
#     print(itema)
# y = yadisk.YaDisk(token=token_yandex)
# y.upload(url, itema.likes + '.jpg')

