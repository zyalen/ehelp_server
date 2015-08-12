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

    resp = {}
    if KEY.OPERATION in params:
      if params[KEY.OPERATION] == 0:
        result = db.sign_in(params)
        resp[KEY.ID] = params[KEY.ID]
        if result:
          resp[KEY.STATUS] = STATUS.OK
        else:
          resp[KEY.STATUS] = STATUS.ERROR
      elif params[KEY.OPERATION] == 1:
        result = db.is_sign_in(params[KEY.ID])
        resp[KEY.ID] = params[KEY.ID]
        resp[KEY.STATUS] = STATUS.OK
        if result:
          resp[KEY.TYPE] = 1
        else:
          resp[KEY.TYPE] = 0
      else:
        resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))