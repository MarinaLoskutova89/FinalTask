import requests
import json


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

    def get_photos(self, owner_id, album_id, count=5):
        all_photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': owner_id,
            'album_id': album_id,
            'extended': 1,
            'photo_sizes': 1,
            'count': count
        }
        res = requests.get(all_photos_url, params={**self.params, **photos_params}).json()
        self.write_json(res['response']['items'])
        return res