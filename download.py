# coding:utf-8
from db.db import Operation
import time
import requests

file_path = 'D:/douyin/'


class Download:

    def __init__(self):
        self.db = Operation()
        self.t = 0
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        }

    def start(self):
        while True:
            tmp = self.db.db.find('data', {'post_youtube': 0})
            if isinstance(tmp, bool):
                pass
            elif isinstance(tmp, dict):
                if self.get(tmp):
                    self.db.db.update('data', {'aweme_id': tmp['aweme_id']}, {'post_youtube': 1})
            elif isinstance(tmp, list):
                for x in tmp:
                    if self.get(x):
                        self.db.db.update('data', {'aweme_id': x['aweme_id']}, {'post_youtube': 1})
            time.sleep(10)

    def get(self, db):
        try:
            tmp = requests.get(db['play_addr'][0], headers=self.headers)
        except:
            return False
        if tmp.status_code == 200:
            if db['desc'].strip():
                file_name = file_path+db['desc']+'.mp4'
            else:
                file_name = file_path + 'nothing'+str(self.t) + '.mp4'
            self.t += 1
            try:
                with open(file_name, 'wb') as f:
                    print('Get:', file_name.split('/')[-1])
                    f.write(tmp.content)
            except OSError:
                with open(file_path+'nothing'+str(self.t)+'.mp4', 'wb') as f:
                    print('Get:', file_name.split('/')[-1])
                    f.write(tmp.content)
            except:
                print('Error')
        return True


Download().start()
