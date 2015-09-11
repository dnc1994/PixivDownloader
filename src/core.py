import os
import requests
from pyquery import PyQuery as pq

SEP = os.sep

class Worker:
    def __init__(self):
        self.session = requests.Session()
        self.login_url = 'https://www.secure.pixiv.net/login.php'
        self.fav_list_url = 'http://www.pixiv.net/bookmark.php?type=user'
        self.member_url = 'http://www.pixiv.net/member.php?id='
        self.member_illust_url = 'http://www.pixiv.net/member_illust.php?id='
    
    def login(self, username, password):
        print 'Login...'
        data = {'mode': 'login', 'pixiv_id': username, 'pass': password, 'skip': 1}
        resp = self.session.post(self.login_url, data=data)
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
    
    def buildFavProfiles(self, fav_id_list):
        pass
        
    def download(self, url, path):
        if (path[len(path) - 1] != os.sep):
            path += os.sep
        if not os.path.exists(path):
            os.makedirs(path)
        # todo: fix path
        if os.path.isfile(path):
            return True
        # todo: handle failure
        data = self.session.get(url).read()
        self.saveFile(data, path)
        return True
        
    def saveFile(self, data, path):
        pass
        
        
class Member:
    def __init__(self):
        pass

class Illust:
    def __init__(self):
        pass

class Manga:
    def __init__(self):
        pass

class Ugoriha:
    def __init__(self):
        pass
