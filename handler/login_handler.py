#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Login_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    if KEY.SALT not in params:
      salt = db.get_salt(params)
      if salt is None:
        resp[KEY.STATUS] = STATUS.ERROR
      else:
        resp[KEY.ACCOUNT] = params[KEY.ACCOUNT]
        resp[KEY.STATUS] = STATUS.OK
        resp[KEY.SALT] = salt
    
    else:
      user_id = db.validate_password(params)
      if user_id > 0:
        resp[KEY.STATUS] = STATUS.OK
        resp[KEY.ACCOUNT] = params[KEY.ACCOUNT]
        resp[KEY.ID] = user_id
      else:
        resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))

    

