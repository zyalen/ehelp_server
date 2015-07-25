__author__ = 'hanks'

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import haversine
from utils import KEY
from utils import STATUS
from database import db

class Get_Neighbor_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    res = {}
    res[KEY.IID_LIST] = db.get_neighbor(params)
    res[KEY.STATUS] = STATUS.OK

    self.write(res)
