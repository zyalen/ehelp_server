#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Add_Event_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    event_id = db.add_event(params)
    if event_id > 0:
      event_info = {}
      event_info[KEY.EVENT_ID] = event_id
      resp = db.get_event_information(event_info)
      if resp is None:
        resp = {}      
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR
      if event_id == -1:
        resp[KEY.VALUE] = -1
      if event_id == -2:
        resp[KEY.VALUE] = -2

    
    self.write(json_encode(resp))

    

