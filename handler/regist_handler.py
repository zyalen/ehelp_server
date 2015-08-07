#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Regist_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    user_id = db.add_account(params)
    resp = {}
    if user_id > 0:
      resp[KEY.STATUS] = STATUS.OK
      resp[KEY.ACCOUNT] = params[KEY.ACCOUNT]
      resp[KEY.ID] = user_id
      resp[KEY.SALT] = db.get_salt(params)
      resp[KEY.CHAT_TOKEN] = db.get_chat_token(params)
      bank_account_id = db.create_loving_bank(resp, 20, 0)
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))

    

