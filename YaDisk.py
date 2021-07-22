import requests
import time
from tqdm import tqdm

class YandexDisk:

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def creat_folders(self,folder_name='Photo from VK'):
        files_url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params = {"path": '/' + folder_name}
        response = requests.put(files_url, headers=headers, params=params)
        print(f'Creating folder "{folder_name}":' + str(response.status_code))


    def upload_files_to_disk(self, disk_file_path, photos):
        self.creat_folders('Photo from VK')
        upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        for key, value in tqdm(photos.items()):
            time.sleep(0.5)
            params = {"path": disk_file_path + '/' + key,
                      "url": value
                     }
            response = requests.post(upload_url, headers=headers, params=params)
            response.raise_for_status()
            if response.status_code == 201:
                print("Success")
