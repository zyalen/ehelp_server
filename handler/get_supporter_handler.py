__author__ = 'hanks'

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Get_Supporter_Handler_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    if KEY.EVENT_ID not in params:
      resp[KEY.STATUS] = STATUS.ERROR
    resp[KEY.USER_LIST] = db.get_supporters(params)
    resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))