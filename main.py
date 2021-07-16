import requests
import json
import os
import yadisk
from dataclasses import dataclass

@dataclass
class VKPic:
    id: str
    size: int
    url: str
    likes: int

with open('token_vk_user.txt', 'r', encoding='utf-8') as file_object:
    token = file_object.read().strip()

with open('token_yandex.txt', 'r', encoding='utf-8') as file_object:
    token_yandex = file_object.read().strip()

#token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'

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
        #return res
        self.write_json(res['response']['items'])
        return res

    # def get_largest_photo(self, size_dict):
    #     if size_dict['width'] >= size_dict['height']:
    #         return size_dict['width']
    #     else:
    #         return size_dict['height']
    #
    # def largest_photo(self, file):
    #     url = []
    #     photos = json.load(open(file))
    #     for photo in photos:
    #         sizes = photo['sizes']
    #         max_photos_url = max(sizes, key=self.get_largest_photo)['url']
    #         url.append(max_photos_url)
    #     return url
    #
    # def make_direct(self, direct):
    #     if not os.path.isdir(direct):
    #         os.mkdir(direct)
    #
    # def download_photo(self, url, filename, direct):
    #     photo_url = url
    #     photo_name = filename
    #     photo = dict(zip(photo_url, photo_name))
    #     self.make_direct(direct)
    #     for key, value in photo.items():
    #         res = requests.get(key, stream=True)
    #         with open(f'{direct}/{value}.jpg', 'wb') as file:
    #             for chunk in res.iter_content(4096):
    #                 file.write(chunk)


vk_client = VKUser(token, '5.131')
data = vk_client.get_photos('552934290', 'profile')
# url = vk_client.largest_photo('response.json')
# filename = vk_client.get_photos_name('response.json')
# itema = vk_client.get_photos_name()
#vk_client.download_photo(url, filename, 'Photo')
#print(data['response']['items'])

list = []
for item in data['response']['items']:
    for size in item['sizes']:
        ss = size['width'] * size['height']
        pic = VKPic(item['id'], ss, size['url'], item['likes']['count'])
        list.append(pic)
        itema = [d for d in list if d.size == max(d.size for d in list)]

y = yadisk.YaDisk(token=token_yandex)
print('Token yandex status:')
print(y.check_token())

y.upload(itema.url, itema.likes + '.jpg')