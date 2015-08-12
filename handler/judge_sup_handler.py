__author__ = 'hanks'

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db

class Judge_Sup(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    judge = db.judge_sup(params)
    if judge == -1:
      resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp[KEY.TYPE] = judge
      resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))