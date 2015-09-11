"""
1. ORM
2. Cache
3. Exception handling
"""

import os
import requests
from pyquery import PyQuery as pq

class Worker:
    def __init__(self):
        self.session = requests.Session()
        self.login_url = 'https://www.secure.pixiv.net/login.php'
        self.fav_list_url = 'http://www.pixiv.net/bookmark.php?type=user'
        self.member_url = 'http://www.pixiv.net/member.php?id='
        self.member_illust_url = 'http://www.pixiv.net/member_illust.php?id='
        # get meta data
        self.metadata = {}
    
    def login(self, username, password):
        print 'Login...'
        data = {'mode': 'login', 'pixiv_id': username, 'pass': password, 'skip': 1}
        resp = self.session.post(url=self.login_url, data=data)
        if resp.text.find('pixiv.user.loggedIn = true') == -1:
            print 'Login Failed'
            return False
        return True
        
    def getFavList(self):
        print 'Getting FavList'
        resp = self.session.get(self.fav_list_url)
        li_list = pq(resp.text)('#search-result ul li')
        input_list = [elem.getchildren()[0] for elem in li_list]
        id_list = [elem.attrib['value'] for elem in input_list]
        print id_list
        return id_list
    
    def getMemberProfile(self, member_id):
        resp = self.session.get(self.member_illust_url + member_id)
        
    def updateFavProfiles(self, fav_id_list):
        update_list = filter(lambda x: x not in self.metadata['cachedFavList'], fav_id_list)
        for fav in update_list:
            pass
            
    def getResList(self, member_id):
        res_list = []
        return res_list
    
    # define failsafe
    @failsafe
    def safeGet(self, url):
        return self.session.get(url)
    
    def downloadToFile(self, res, path):
        # check type
        url = res.url
        if (path[len(path) - 1] != os.sep):
            path += os.sep
        path += res.path
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.isfile(path):
            return True
        try:
            data = safeGet(url)
            # save file
            self.saveFile(data, path)
            return True
        except:
            return False
    
    def downloadRes(self, res_id, path):
        # check res type (?) and create objects
        if a:
            res = Illust(name, url)
        if b:
            res = Mange(name, url)
        if c:
        if type(res) == Illust:
            downloadToFile(res, path)
        if type(res) == Manga:
            for illust in res.pages:
                downloadToFile(res, path)
        if type(res) == Ugoriha:
            downloadToFile(res)
    
    def bulkDownload(self, res_list, path):
        for res in res_list:
            downloadRes(res)
        
        
class Member:
    def __init__(self, id):
        self.member_id = id
        
class Illust:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.path = ''
        self.getProperLink()
        self.fixPath()
        
    def getProperLink(self):
        # get the link to largest possible illust
        
    def fixPath(self):
        # use author info to fix res.path

class Manga(Illust):
    def __init__(self, name, url, path):
        (super)self.__init__(name, url, path)
        self.path += self.name os.sep
        self.pages = []
        # get page list

# figure out the difference        
class Ugoriha(Illust):
    def __init__(self):
        pass
