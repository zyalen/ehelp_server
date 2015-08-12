__author__ = 'hanks'

import urllib
import httplib
import hashlib
import random
import time
'''
get chat_token from RongCloud
@param includes: id, user's id, a unique id
       options:  nickname, user's nickname
                 imgUri, the uri of image
@return chat_token
        None if fails
'''
def getToken(id, nickname, imgUri):

  # use sha1 to generate the signature
  nonce = random.randint(0, 99999)
  timestamp = int(time.mktime(time.localtime()))
  appkey = '0vnjpoadn5kxz'
  appsecret = 'GTTmlirESMO8'
  signature = hashlib.sha1(appsecret + str(nonce) + str(timestamp)).hexdigest()

  # the request info
  test_data = {'userId': id, 'name': nickname, 'portraitUri': imgUri}
  test_data_urlencode = urllib.urlencode(test_data)
  requrl = "https://api.cn.ronghub.com/user/getToken.json"
  headerdata = {'Host': 'api.cn.ronghub.com', 'App-Key': appkey,
              'Nonce': nonce, 'Timestamp': timestamp,
              'Signature': signature,
              'Content-Type': 'application/x-www-form-urlencoded'}

  conn = httplib.HTTPSConnection('api.cn.ronghub.com')
  conn.request(method='POST', url=requrl, body=test_data_urlencode, headers=headerdata)

  # return the token, or the error message if fails
  responce = conn.getresponse()
  res = eval(responce.read())

  if 'token' in res:
    return res['token']
  else:
    return None
