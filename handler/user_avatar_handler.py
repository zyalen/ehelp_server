__author__ = 'thetruthmyg'

from tornado.web import RequestHandler
from tornado.escape import json_encode

from utils import utils
from utils import KEY
from utils import STATUS
from database import db

'''
upload avatar for the account
@params a text as avatar's name and a file
    which is a picture.
'''
class UploadAvatar_Handler(RequestHandler):
  def post(self):
    filename = self.get_body_argument('filename')
    myfile = self.request.files['avatar'][0]
    upload_path = "./static/avatar/" + filename
    fin = open(upload_path, "w")
    res = fin.write(myfile["body"])
    fin.close()

    resp = {}
    if res is None:
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR

    self.write(json_encode(resp))