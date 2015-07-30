#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class User_Relation_Manage_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    if KEY.OPERATION not in params:
      resp[KEY.STATUS] = STATUS.ERROR
    elif params[KEY.OPERATION] == 0:
      if db.remove_static_relation(params):
        resp[KEY.STATUS] = STATUS.OK
      else:
        resp[KEY.STATUS] = STATUS.ERROR
    elif params[KEY.OPERATION] == 1:
      if db.add_static_relation(params):
        resp[KEY.STATUS] = STATUS.OK
      else:
        resp[KEY.STATUS] = STATUS.ERROR
    elif params[KEY.OPERATION] == 2:
      resp[KEY.USER_LIST] = db.query_static_relation(params)
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))

    

