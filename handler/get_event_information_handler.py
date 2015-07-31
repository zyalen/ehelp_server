__author__ = 'thetruthmyg'

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Get_Event_Information_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    resp = {}
    event_info = db.get_event_information(params)
    if event_info is None:
      resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp.update(event_info)
      resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))