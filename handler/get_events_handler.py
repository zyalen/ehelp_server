__author__ = 'hanks'

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Get_Events_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    resp[KEY.EVENT_LIST] = db.get_events(params, db.get_all_events)
    resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))