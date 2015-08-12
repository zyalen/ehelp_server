#!/usr/python

import tornado
import tornado.httpserver
import os
import sys

from handler import regist_handler
from handler import login_handler
from handler import get_user_information_handler
from handler import modify_user_information_handler
from handler import modify_password_handler
from handler import add_event_handler
from handler import update_event_handler
from handler import remove_event_handler
from handler import get_launch_events_handler
from handler import get_join_events_handler
from handler import user_event_manage_handler
from handler import add_comment_handler
from handler import remove_comment_handler
from handler import get_comments_handler
from handler import add_health_handler
from handler import get_health_records_handler
from handler import add_illness_handler
from handler import get_illness_records_handler
from handler import user_relation_manage_handler
from handler import sign_in_handler
from handler import user_avatar_handler
from handler import get_neighbor
from handler import get_nearby_event_handler
from handler import evaluate_handler
from handler import loving_bank_handler
from handler import manage_answer_handler
from handler import get_event_information_handler
from handler import get_supporter_handler
from handler import update_health_handler
from handler import user_bank_manage_handler
from handler import bank_transfer_handler
from handler import get_chat_token_handler
from handler import get_events_handler
from handler import check_transfer_handler
from handler import check_trade_handler

os.chdir(os.path.join(os.getcwd(), os.path.dirname(sys.argv[0])))

def main():
  port = 1501
  application = tornado.web.Application(
    handlers=[
      (r"/account/regist", regist_handler.Regist_Handler),
      (r"/account/login", login_handler.Login_Handler),
      (r"/user/get_information", get_user_information_handler.Get_User_Information_Handler),
      (r"/user/modify_information", modify_user_information_handler.Modify_User_Information_Handler),
      (r"/account/modify_password", modify_password_handler.Modify_Password_Handler),
      (r"/user/upload_avatar", user_avatar_handler.UploadAvatar_Handler),
      (r"/user/neighbor", get_neighbor.Get_Neighbor_Handler),
      (r"/event/add", add_event_handler.Add_Event_Handler),
      (r"/event/modify", update_event_handler.Update_Event_Handler),
      (r"/event/remove", remove_event_handler.Remove_Event_Handler),
      (r"/event/query_launch", get_launch_events_handler.Get_Launch_Events_Handler),
      (r"/event/get_nearby_event", get_nearby_event_handler.Get_Nearby_Event_handler),
      (r"/event/query_join", get_join_events_handler.Get_Join_Events_Handler),
      (r"/user/event_manage", user_event_manage_handler.User_Event_Manage_Handler),     
      (r"/comment/add", add_comment_handler.Add_Comment_Handler),
      (r"/comment/remove", remove_comment_handler.Remove_Comment_Handler),
      (r"/comment/query", get_comments_handler.Get_Comments_Handler),
      (r"/user/relation_manage", user_relation_manage_handler.User_Relation_Manage_Handler),      
      (r"/health/upload", add_health_handler.Add_Health_Handler),
      (r"/health/query", get_health_records_handler.Get_Health_Records_Handler),
      (r"/illness/upload", add_illness_handler.Add_Illness_Handler),
      (r"/illness/query", get_illness_records_handler.Get_Illness_Records_Handler),
      (r"/user/evaluate", evaluate_handler.Evaluate_Handler),
      (r"/account/signin", sign_in_handler.Sign_In_Handler),
      (r"/user/lovingbank", loving_bank_handler.Get_Loving_Bank_Information_Handler),
      (r"/event/add_ans", manage_answer_handler.Add_Answer_Handler),
      (r"/event/anslist", manage_answer_handler.Get_Answerlist_Handler),
      (r"/event/get_information", get_event_information_handler.Get_Event_Information_Handler),
      (r"/event/update_answer", manage_answer_handler.Update_AnswerInformation_Handler),
      (r"/event/get_supporter", get_supporter_handler.Get_Supporter_Handler_Handler),
      (r"/health/update", update_health_handler.Update_Health_Handler),
      (r"/user/bank_manage", user_bank_manage_handler.User_Bank_Manage_Handler),
      (r"/user/bank_transfer", bank_transfer_handler.Bank_Transfer_Handler),
      (r"/account/get_token", get_chat_token_handler.Get_Chat_Token_Handler),
      (r"/event/get_events", get_events_handler.Get_Events_Handler),
      (r"/user/check_trans", check_transfer_handler.Check_Transfer_Handler),
      (r"/user/check_trade", check_trade_handler.Check_Transfer_Handler),
      (r"/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
    ], debug=True)
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(port)


  tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
  main()
