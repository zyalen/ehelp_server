__author__ = 'hanks'


from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class User_Bank_Manage_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    if db.update_loving_bank(params):
      user = {}
      user[KEY.USER_ID] = params[KEY.ID]
      resp = db.get_user_loving_bank(user)
      if resp is not None:
        resp[KEY.STATUS] = STATUS.OK
      else:
        resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp[KEY.STATUS] = STATUS.ERROR

    self.write(json_encode(resp))