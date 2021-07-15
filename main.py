import requests
import json
import os
from yadisk import YaDisk

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

    def get_largest_photo(self, size_dict):
        if size_dict['width'] >= size_dict['height']:
            return size_dict['width']
        else:
            return size_dict['height']

    def largest_photo(self, file):
        url = []
        photos = json.load(open(file))
        for photo in photos:
            sizes = photo['sizes']
            max_photos_url = max(sizes, key=self.get_largest_photo)['url']
            url.append(max_photos_url)
        return url

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

    def get_photos_name(self, file):
        photo_likes = []
        photo_date = []
        filename = json.load(open(file))
        for name in filename:
            photo_likes.append(str(name['likes']['count']))
            photo_date.append(str(name['date']))
        return photo_likes



vk_client = VKUser(token, '5.131')
data = vk_client.get_photos('552934290', 'profile')
url = vk_client.largest_photo('response.json')
filename = vk_client.get_photos_name('response.json')
vk_client.download_photo(url, filename, 'Photo')


class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def get_files_list(self):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
        headers = self.get_headers()
        response = requests.get(files_url, headers=headers)
        return response.json()

    def _get_upload_link(self, disk_file_path):
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        return response.json()

    def upload_file_to_disk(self, disk_file_path, filename):
        href = self._get_upload_link(disk_file_path=disk_file_path).get("href", "")
        response = requests.put(href, data=open(filename, 'rb'))
        response.raise_for_status()
        if response.status_code == 201:
            print("Success")

ya = YandexDisk(token=token_yandex)
ya.upload_file_to_disk(disk_file_path = '',
                           filename = '')