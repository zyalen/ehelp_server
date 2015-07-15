__author__ = 'thetruthmyg'

from tornado.web import RequestHandler
from tornado.escape import json_encode

from utils import utils
from utils import KEY
from utils import STATUS
from database import db


'''
upload avatar for the account
@params a dict data:
    include a user_id,url with the location of the avatar in server.
@return true if upload successfully
    False if failed
'''
class UploadAvatar_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    result = db.upload_avatar(params)
    resp = {}
    if result:
      resp[KEY.STATUS] = STATUS.OK
      resp[KEY.ID] = params[KEY.ID]
    else:
      resp[KEY.STATUS] = STATUS.ERROR

    self.write(json_encode(resp))



'''
get location of user's avatar
@params a dict data:
    include a user_id.
@return the location of the avatar stored in remote host.
    None if failed.
'''


class GetAvatar_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    resp = {}
    user_avatar = db.get_avatar(params)
    if user_avatar is None:
      resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp.update(user_avatar)
      resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))