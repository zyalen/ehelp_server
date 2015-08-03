#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Get_Health_Records_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    if KEY.ID in params:
      records = db.get_health_record(params[KEY.ID])
      if records is None:
        resp[KEY.STATUS] = STATUS.ERROR
      else:
        resp = records
        resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))



