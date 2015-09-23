"""
TODO
1. ORM/Cache
2. Exception handling
"""

import os
import re
import requests
from pyquery import PyQuery as pq
import pickle

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
        return id_list
    
    # further todo
    def getMemberProfile(self, member_id):
        resp = self.req.get(self.member_illust_url + member_id)        
    
    # further todo
    def updateFavProfiles(self, fav_id_list):
        update_list = filter(lambda x: x not in self.metadata['cachedFavList'], fav_id_list)
        for fav in update_list:
            pass
    
    # todo
    def getResList(self, member_id):
        res_list = []
        return res_list
    
    def downloadToFile(self, res, path):
        assert type(res) == Illust
        if (path[len(path) - 1] != os.sep):
            path += os.sep
        path += res.path
        if os.path.isfile(path):
            return True
        folder_path = ''.join(path.split(os.sep)[:-1])
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        try:
            data = self.req.get(res.url)
            with open(path, 'wb') as f:
                f.write(data)
            return True
        except:
            return False        
        
    def parseRes(self, url):
        info = {}
        info['type'] = 'manga' if 'manga' in url else 'illust'
        id = re.search(r'id=(\d+)', url).group(1)
        resp = self.req.get(url)
        img = pq(resp.text)('.original-image')[0]
        title = pq(resp.text)('.work-info h1.title')[0]
        user = pq(resp.text)('h1.user')[0]
        info['title'] = id + '_' + title.text
        info['user'] = user.text
        info['link'] = img.attrib['data-src']
        return info
    
    def createIllust(self, info, folder=None)
        filename = info['link'].split('/')[-1]
        extension = filename[filename.find('.'):]
        path = [info['user']]
        if folder:
            path.append(folder)
        path.append(info['title'] + extension)
        return Illust(info['title'], info['link'], path)
        
    def createRes(self, info):
        if info['type'] == 'illust':
            return self.createIllust(info)
        if info['type'] == 'manga':
            from_url = info['link']
            pages_url = []
            pages_info = [parseRes(page_url) for page_url in pages_url]
            manga = Manga(info['title'], info['link'], path)
            manga.pages = [self.createIllust(page_info, info['title']) for page_info in pages_info]            
            return manga
    
    def downloadRes(self, res_url, path):
        info = parseRes(res_url)
        res = createRes(info)
        if type(res) == Illust:
            self.downloadToFile(res, path)
        if type(res) == Manga:
            for illust in res.pages:
                self.downloadToFile(illust, path)
    
    def bulkDownload(self, res_url_list, path):
        for res_url in res_url_list:
            self.downloadRes(res_url, path)  
        
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
    def __init__(self, name, url, path, pages=None):
        super(Manga, self).__init__(name, url, path)
        self.pages = pages

# todo        
class Ugoriha(Illust):
    def __init__(self, name, url, path):
        super(Ugoriha, self).__init__(name, url, path)
