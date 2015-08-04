#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Remove_Event_Handler(RequestHandler):
  def post(self):
    print self
    params = utils.decode_params(self.request)
    
    resp = {}
    result = db.remove_event(params)
    if KEY.EVENT_ID in params:
      resp[KEY.EVENT_ID] = params[KEY.EVENT_ID]
    if result:
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))

    

