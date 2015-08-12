__author__ = 'hanks'

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db

class Check_Transfer_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    h_list = db.check_transfer(params)
    if h_list == -1:
      resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp[KEY.H_LIST] = h_list
      resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))