__author__ = 'thetruthmyg'

from tornado.web import RequestHandler
from tornado.escape import json_encode

from utils import KEY
from utils import STATUS

import re

img_pattern = re.compile(r'(\W|\w)*(.jpg|.png|.bmp)', re.S)
vid_pattern = re.compile(r'(\W|\w)*(.mp4|.3gp|.avi)', re.S)
sou_pattern = re.compile(r'(\W|\w)*(.mp3|.wav|.amr)', re.S)

'''
upload avatar for the account
@params a text as avatar's name and a file
    which is a picture, video or sound.
'''
class UploadAvatar_Handler(RequestHandler):
  def post(self):
    myfile = self.request.files['avatar'][0]
    filename = myfile['filename']
    index = filename.rfind('\\')
    if index != -1:
      filename = filename[index + 1:]
    if re.match(img_pattern, filename):
      upload_path = "./static/avatar/" + filename
    elif re.match(vid_pattern, filename):
      upload_path = "./static/video/" + filename
    elif re.match(sou_pattern, filename):
      upload_path = "./static/sound/" + filename
    fin = open(upload_path, "wb")
    res = fin.write(myfile["body"])
    fin.close()

    resp = {}
    if res is None:
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR

    self.write(json_encode(resp))