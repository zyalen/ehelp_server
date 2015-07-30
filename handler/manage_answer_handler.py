__author__ = 'thetruthmyg'
#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db

class Add_Answer_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    answer_id = db.add_answer(params)
    if answer_id > 0:
      answer_info = {}
      answer_info[KEY.ANSWER_ID] = answer_id
      resp = db.get_answer_info(answer_info)
      if resp is None:
        resp = {}
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR

    self.write(json_encode(resp))


class Get_Answerlist_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    resp[KEY.ANSWER_LIST] = db.get_answers(params, db.get_answer_id_list)
    resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))