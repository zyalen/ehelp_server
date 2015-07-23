#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Sign_In_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    result = db.sign_in(params)
    resp = {}
    resp[KEY.ID] = params[KEY.ID]
    if result:
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))