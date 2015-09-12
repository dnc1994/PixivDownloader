"""
TODO
1. ORM/Cache
2. Exception handling
"""

import os
import requests
from pyquery import PyQuery as pq

class Worker:
    def __init__(self):
        self.req = requests.Session()
        self.login_url = 'https://www.secure.pixiv.net/login.php'
        self.fav_list_url = 'http://www.pixiv.net/bookmark.php?type=user'
        self.member_url = 'http://www.pixiv.net/member.php?id='
        self.member_illust_url = 'http://www.pixiv.net/member_illust.php?id='
        # get meta data
        self.metadata = {}
    
    def login(self, username, password):
        print 'Login...'
        data = {'mode': 'login', 'pixiv_id': username, 'pass': password, 'skip': 1}
        resp = self.req.post(url=self.login_url, data=data)
        if resp.text.find('pixiv.user.loggedIn = true') == -1:
            print 'Login Failed'
            return False
        return True
        
    def getFavList(self):
        print 'Getting FavList'
        resp = self.req.get(self.fav_list_url)
        li_list = pq(resp.text)('#search-result ul li')
        input_list = [elem.getchildren()[0] for elem in li_list]
        id_list = [elem.attrib['value'] for elem in input_list]
        print id_list
        return id_list
    
    def getMemberProfile(self, member_id):
        resp = self.req.get(self.member_illust_url + member_id)
        
    def updateFavProfiles(self, fav_id_list):
        update_list = filter(lambda x: x not in self.metadata['cachedFavList'], fav_id_list)
        for fav in update_list:
            pass
            
    def getResList(self, member_id):
        res_list = []
        return res_list
    
    def downloadToFile(self, res, path):
        assert type(res) == Illust
        url = res.url
        if (path[len(path) - 1] != os.sep):
            path += os.sep
        path += res.path
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.isfile(path):
            return True
        try:
            data = self.req.get(url)
            with open(path, 'wb') as f:
                f.write(data)
            return True
        except:
            return False        
        
    def parseRes(self, url):
        info = {}
        info['type'] = 'manga' if 'manga' in url else 'illust'
        resp = self.req.get(url)
        img = pq(resp.text)('.original-image')[0]
        title = pq(resp.text)('.work-info h1.title')[0]
        user = pq(resp.text)('h1.user')[0]
        info['title'] = title.text
        info['user'] = user.text
        info['link'] = img.attrib['data-src']
        return info
    
    # todo
    def createRes(self, info):
        if info['type'] == 'illust':
            pass
        if info['type'] == 'manga':
            pass
    
    def downloadRes(self, res_url, path):
        info = parseRes(res_url)
        res = createRes(info)
        if type(res) == Illust:
            downloadToFile(res, path)
        if type(res) == Manga:
            for illust in res.pages:
                downloadToFile(illust, path)
    
    def bulkDownload(self, res_url_list, path):
        for res_url in res_url_list:
            downloadRes(res_url, path)  
        
class Member:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        
class Illust:
    def __init__(self, name, url, path):
        self.name = name
        self.url = url
        self.path = os.sep.join(path)

class Manga(Illust):
    def __init__(self, name, url, path, pages):
        super(Manga, self).__init__(name, url, path)
        self.pages = pages

# todo        
class Ugoriha(Illust):
    def __init__(self):
        pass
