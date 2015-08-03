#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Add_Health_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    if KEY.ID in params:
      health_id = db.health_record(params)
      if health_id > 0:
        resp = db.get_health_record(params[KEY.ID])
        if resp is None:
          resp = {}
        resp[KEY.STATUS] = STATUS.OK
      else:
        resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))

    

