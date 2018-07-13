# coding:utf-8
import requests
import demjson
from api import *
from logzero import logger
import time
from db import db


class Main:
    init_userid = ['69659037176']
    visited_userid = []
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    }

    def __init__(self):
        self.db = db.Operation()
        # self.db.db.find()

    def main(self):
        while True:
            try:
                userid = self.init_userid.pop(0)
                self.visited_userid.append(userid)
            except IndexError:
                logger.error('Complete')
                break
            data = self.get_like(userid)
            if data:
                for x in data:
                    user_id_new = self.get_userid(x['aweme_id'])
                    if user_id_new:
                        x['userid'] = user_id_new
                        if (user_id_new not in self.init_userid) and (user_id_new not in self.visited_userid):
                            self.init_userid.append(user_id_new)
                    if not self.db.db.find('data', {'aweme_id': x['aweme_id']}):
                        self.db.db.save('data', x)
                    # logger.info(x)
            else:
                logger.error('error  ' + str(userid))

    def get_like(self, userid):
        getlike = 'https://www.amemv.com/aweme/v1/aweme/favorite/?user_id={0}&count={1}'
        count = 3000
        while True:
            try:
                result = demjson.decode(requests.get(getlike.format(str(userid), str(count)), headers=self.headers).text, encoding='utf-8')
            except demjson.JSONDecodeError:
                return False
            except requests.exceptions.ConnectTimeout:
                return False
            if result['status_code'] == 0:
                if result['has_more'] == 0:
                    break
                else:
                    count += 1000
            else:
                return False
        data = []
        for x in result['aweme_list']:
            try:
                tmp = {
                    'aweme_id': x['aweme_id'],
                    'short_id': x['author']['short_id'],
                    'play_addr': x['video']['play_addr']['url_list'],
                    'desc': x['desc'].strip(),
                    'create_time': x['create_time'],
                    'get_time': time.time(),
                    'like_count': x['statistics']['digg_count'],
                    'post_youtube': 0
                }
                data.append(tmp)
            except KeyError:
                pass
        return data

    def get_userid(self, aweme_id):
        res = requests.get(awemeid_to_userid.format(str(aweme_id)), headers=self.headers).text
        try:
            result = demjson.decode(res, encoding='utf-8')
        except demjson.JSONDecodeError:
            return False
        except requests.exceptions.ConnectTimeout:
            return False
        if result['status_code'] == 0:
            try:
                return result['aweme_detail']['author_user_id']
            except KeyError:
                return False
        else:
            return False


if __name__ == '__main__':
    a = Main()
    a.main()
    # import threading
    # a = Main()
    # for x in range(2):
    #     t = threading.Thread(target=a.main)
    #     t.setDaemon(True)
    #     t.start()
    #     time.sleep(10)
