from pprint import pprint
import requests
import json
from yadisk import YaDisk

with open('token_vk_user.txt', 'r', encoding='utf-8') as file_object:
    token = file_object.read().strip()


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

    def get_largest_photo(self, size_dict):
        if size_dict['width'] >= size_dict['height']:
            return size_dict['width']
        else:
            return size_dict['height']

    def largest_photo(self, file):
        photos = json.load(open(file))
        for photo in photos:
            sizes = photo['sizes']
            max_photos_url = max(sizes, key=self.get_largest_photo)['url']
            self.download_photo(max_photos_url)

    def download_photo(self, url, filename):
        res = requests.get(url, stream=True)
        with open(filename, 'wb') as file:
            for chunk in res.iter_content(4096):
                file.write(chunk)

    def get_photos_name(self, file):
        photo_likes = []
        photo_date = []
        filename = json.load(open(file))
        for name in filename:
            photo_likes.append(name['likes']['count'])
            photo_date.append(name['date'])
            return

vk_client = VKUser(token, '5.131')
vk_client.get_photos('552934290', 'profile')
# vk_client.largest_photo()
vk_client.get_photos_name('response.json')

