#!/usr/python

import sys
sys.path.append("..")
import random
import string
import hashlib
import MySQLdb
import ast
import traceback

from dbhelper import dbhelper
from utils import haversine
from utils import KEY
from utils import getToken

  
'''
add a new account to database.
@params a dict data:
        includes account and password.
@return -1 indicates params are not complete. Or account is not unique that leads to database fails.
        other number indicates success and the number is the id of the new account.
'''
def add_account(data):
  if KEY.ACCOUNT not in data or KEY.PASSWORD not in data:
    return -1
  
  salt = ''.join(random.sample(string.ascii_letters, 8))
  md5_encode = hashlib.md5()
  md5_encode.update(data[KEY.PASSWORD]+salt)
  password = md5_encode.hexdigest()

  sql_account = "insert into account (account, password, salt) values ('%s', '%s', '%s')"
  sql_user = "insert into user (id, nickname, phone) values (%d, '%s', '%s')"
  try:
    insert_id = dbhelper.insert(sql_account%(data[KEY.ACCOUNT], password, salt))
    dbhelper.insert(sql_user%(insert_id, data[KEY.ACCOUNT], data[KEY.ACCOUNT]))
    chat_token = getToken.getToken(insert_id, None, None)
    sql_chat = "update account set chat_token = '%s' where id = %d"
    dbhelper.execute(sql_chat%(chat_token, insert_id))
    return insert_id
  except Exception, e:
    print e
    return -1


'''
update information of an account.
@params a dict data:
        includes id and chat_token:
@return True if successfully modify chat_token
        False modification fails.
'''
def update_account(data):
  if KEY.ID in data and KEY.CHAT_TOKEN in data:
    sql = "update account set chat_token = '%s' where id = %d"
    try:
      if dbhelper.execute(sql%(data[KEY.CHAT_TOKEN], data[KEY.ID])) > 0:
        return True
    except:
      return False
  else:
    return False


'''
modify user's information.
@params a dict data:
        options include user's name, nickname, gender, age, phone, location,
        (longitude and latitude), occupation, identity_id.
@return True if successfully modify
        False modification fails.
'''
def update_user(data):
  if KEY.ID not in data:
    return False
  result = True
  
  sql = ""
  if KEY.NAME in data:
    data[KEY.NAME] = MySQLdb.escape_string(data[KEY.NAME].encode("utf8"))
    sql = "update user set name = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.NAME], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.NICKNAME in data:
    data[KEY.NICKNAME] = MySQLdb.escape_string(data[KEY.NICKNAME].encode("utf8"))
    sql = "update user set nickname = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.NICKNAME], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.GENDER in data:
    sql = "update user set gender = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.GENDER], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.AGE in data:
    sql = "update user set age = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.AGE], data[KEY.ID]))
      result &= True
    except:
      result &= False
   
  if KEY.PHONE in data:
    sql = "update user set phone = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.PHONE], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.LOCATION in data:
    data[KEY.LOCATION] = MySQLdb.escape_string(data[KEY.LOCATION].encode("utf8"))
    sql = "update user set location = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LOCATION], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.LONGITUDE in data and KEY.LATITUDE in data:
    sql = "update user set longitude = %f, latitude = %f where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LONGITUDE], data[KEY.LATITUDE], data[KEY.ID]))
      result &= True
    except:
      result &= False
  elif not (KEY.LONGITUDE not in data and KEY.LATITUDE not in data):
    result &= False

  if KEY.OCCUPATION in data:
    sql = "update user set occupation = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.OCCUPATION], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.IDENTITY_ID in data:
    sql = "update user set identity_id = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.IDENTITY_ID], data[KEY.ID]))
      result &= True
    except:
      result &= False

  return result


'''
get salt of an account.
@params include user's account.
@return salt of an account.
  None if account not exists or database query error.
'''
def get_salt(data):
  if KEY.ACCOUNT not in data:
    return None
  sql = "select salt from account where account = '%s'"
  try:
    res = dbhelper.execute_fetchone(sql%(data[KEY.ACCOUNT]))
    if res is None:
      return None
    else:
      return res[0]
  except:
    return None


'''
validate whether password is correct.
@params includes user's account and password.
                      password need to be md5 encode.
@return user's id if password is correct.
         -1 otherwise.
'''
def validate_password(data):
  if KEY.ACCOUNT not in data or KEY.PASSWORD not in data or KEY.SALT not in data:
    return -1
  sql = "select id, password from account where account = '%s' and salt = '%s'"
  user_id = -1
  password = None
  try:
    res = dbhelper.execute_fetchone(sql%(data[KEY.ACCOUNT], data[KEY.SALT]))
    if res is not None:
      user_id = res[0]
      password = res[1]
  except:
    pass
  finally:
    if password is None or data[KEY.PASSWORD] is None:
      return -1
    elif password == data[KEY.PASSWORD]:
      return user_id
    else:
      return -1


'''
modify user's password to a new one, but not modify its salt value.
@params include user's account. 
                      new password that encode with salt by md5.
@return true if successfully modify.
           false otherwise.
'''
def modify_password(data):
  if KEY.ACCOUNT not in data or KEY.PASSWORD not in data:
    return False
  sql = "update account set password = '%s' where account = '%s'" 
  try:
    n = dbhelper.execute(sql%(data[KEY.PASSWORD], data[KEY.ACCOUNT]))
    if n > 0:
      return True
    else:
      return False
  except:
      return False
  
  
'''
get user's information, which includes user's name, nickname, gender ...... .
@params include user's id
        option user's phone
@return a json includes user's concrete information.
           None if params error or database query error.
'''
def get_user_information(data):
  if KEY.ID not in data:
    if KEY.PHONE not in data:
      return None
    else:
      sql = "select * from user where phone = %s"%(data[KEY.PHONE])
  else:
    sql = "select * from user where id = %d"%(data[KEY.ID])
  try:
    res = dbhelper.execute_fetchone(sql)
    if res is None:
      return None
    else:
      user = {}
      user[KEY.ID] = res[0]
      user[KEY.NAME] = res[1]
      user[KEY.NICKNAME] = res[2]
      user[KEY.GENDER] = res[3]
      user[KEY.AGE] = res[4]
      user[KEY.PHONE] = res[5]
      user[KEY.LOCATION] = res[6]
      user[KEY.LONGITUDE] = float(res[7])
      user[KEY.LATITUDE] = float(res[8])
      user[KEY.OCCUPATION] = res[9]
      user[KEY.REPUTATION] = float(res[10])
      user[KEY.IDENTITY_ID] = res[12]
      user[KEY.IS_VERIFY] = res[14]
      user[KEY.FOLLOW] = 0
      user[KEY.FOLLOWER] = 0

      user_a = {'id': user[KEY.ID], 'state': 0}
      follow = query_follow(user_a)
      if follow != -1:
        user[KEY.FOLLOW] = len(follow)
      user_b = {'id': user[KEY.ID], 'state': 1}
      follower = query_follow(user_b)
      if follower != -1:
        user[KEY.FOLLOWER] = len(follower)

      return user
  except:
    return None


'''
launch a help event by launcher.
@params includes user's id and type of help event.
        help event types:
                         0 represents normal question.
                         1 represents nornal help.
                         2 represents emergency.
       other option params includes content of event, longitude and latitude of event.
@return event_id if successfully launches.
        -1 if fails.
        -2 if lack love_coin
'''
def add_event(data):
  if KEY.ID not in data or KEY.TYPE not in data or KEY.TITLE not in data:
    return -1
  if KEY.LOVE_COIN in data:
    if exchange(data) == False:
      return False
  sql = "insert into event (launcher, type, time) values (%d, %d, now())"
  event_id = -1
  try:
    event_id = dbhelper.insert(sql%(data[KEY.ID], data[KEY.TYPE]))
    if event_id > 0:
      data[KEY.EVENT_ID] = event_id
      if not update_event(data):
        return -1
    return event_id
  except:
    return -1


'''
modify information of a help event.
@params  includes event_id, which is id of the event to be modified.
         option params includes: title of event, content of event, longitude and latitude of event, state of event,
         the number of the demand person, the number of the love_coin to paid, the comment of the event.
@return True if successfully modifies.
        False otherwise.
'''
def update_event(data):
  result = True
  if KEY.EVENT_ID not in data:
    return False
  sql = ""
  if KEY.TITLE in data:
    data[KEY.TITLE] = MySQLdb.escape_string(data[KEY.TITLE].encode("utf8"))
    sql = "update event set title = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.TITLE], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False
  if KEY.CONTENT in data:
    data[KEY.CONTENT] = MySQLdb.escape_string(data[KEY.CONTENT].encode("utf8"))
    sql = "update event set content = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.CONTENT], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False
  
  if KEY.LONGITUDE in data and KEY.LATITUDE in data:
    sql = "update event set longitude = %f, latitude = %f where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LONGITUDE], data[KEY.LATITUDE], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False

  if KEY.STATE in data:
    if data[KEY.STATE] == 0:
      data[KEY.STATE] = 1
    sql = "update event set state = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.STATE], data[KEY.EVENT_ID]))
      if reward(data):
        result &= True
      else:
        result &= False
    except:
      result &= False

  if KEY.DEMAND_NUMBER in data:
    sql = "update event set demand_number = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.DEMAND_NUMBER], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False

  if KEY.LOVE_COIN in data:
    sql = "update event set love_coin = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LOVE_COIN], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False

  if KEY.COMMENT in data:
    data[KEY.COMMENT] = MySQLdb.escape_string(data[KEY.COMMENT].encode("utf8"))
    sql = "update event set comment = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.COMMENT], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False

  if KEY.LOCATION in data:
    data[KEY.LOCATION] = MySQLdb.escape_string(data[KEY.LOCATION].encode("utf8"))
    sql = "update event set location = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LOCATION], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False
  return result


'''
remove a help event by event launcher.
@params includes user's id, which is remover. Actually, only the launcher can remove his/her event.
                 event's id, which represents the event to be removed.
@return True if successfully removes, or remover is not the launcher, actually nothing happens.
        False if fails.
'''
def remove_event(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data:
    return False
  sql = "delete from event where id = %d and launcher = %d"
  try:
    dbhelper.execute(sql%(data[KEY.EVENT_ID], data[KEY.ID]))
    return True
  except:
    return False


'''
get information of a help event.
@params includes id of the event to get.
@return concrete information of the event:
        event_id, launcher's id and his/her nickname, content, type, time, longitude and latitude, state, number of followers, number of supporters and group points.
        None indicates fail query.
'''
def get_event_information(data):
  if KEY.EVENT_ID not in data:
    return None
  event_info = None
  sql = "select * from event where id = %d"
  try:
    sql_result = dbhelper.execute_fetchone(sql%(data[KEY.EVENT_ID]))
    if sql_result is not None:
      event_info = {}
      event_info[KEY.EVENT_ID] = sql_result[0]
      event_info[KEY.LAUNCHER_ID] = sql_result[1]
      event_info[KEY.TITLE] = sql_result[2]
      event_info[KEY.CONTENT] = sql_result[3]
      event_info[KEY.TYPE] = sql_result[4]
      event_info[KEY.TIME] = str(sql_result[5])
      event_info[KEY.LAST_TIME] = str(sql_result[6])
      event_info[KEY.LONGITUDE] = float(sql_result[7])
      event_info[KEY.LATITUDE] = float(sql_result[8])
      event_info[KEY.STATE] = sql_result[9]

      event = {}
      event[KEY.EVENT_ID] = sql_result[0]
      event[KEY.TYPE] = 1
      event_info[KEY.FOLLOW_NUMBER] = len(get_supporters(event))
      event[KEY.TYPE] = 2
      event_info[KEY.SUPPORT_NUMBER] = len(get_supporters(event))

      event_info[KEY.GROUP_PTS] = float(sql_result[12])
      event_info[KEY.DEMAND_NUMBER] = sql_result[13]
      event_info[KEY.LOVE_COIN] = sql_result[14]
      event_info[KEY.COMMENT] = sql_result[15]
      event_info[KEY.LOCATION] = sql_result[16]
      user = {}
      user[KEY.ID] = event_info[KEY.LAUNCHER_ID]
      user = get_user_information(user)
      if user is not None:
        event_info[KEY.LAUNCHER] = user[KEY.NICKNAME]
  except:
    pass
  finally:
    return event_info


'''
get information of a collection of events.
@params includes data, a json that contains user's id and type of events to get.
                 get_event_id_list a method of getting event id list.
@return a array of events. each element is information of an event in json form.
'''
def get_events(data, get_event_id_list):
  event_id_list = get_event_id_list(data)
  event_list = []
  event_info = {}
  for event_id in event_id_list:
    event_info[KEY.EVENT_ID] = event_id
    event_info = get_event_information(event_info)
    if event_info is not None:
      event_list.append(event_info)
  return event_list

'''
get events that launch by user.
@params includes user's id,
                 option params includes state indicates all events or those starting or ended.
                 type indicates type of events.
                 last_time indicates the last time client update
@return an array of result event ids.
'''
def get_launch_event_list(data):
  event_id_list = []
  if KEY.ID not in data:
    return event_id_list
  sql = "select id from event where launcher = %d"%data[KEY.ID]
  if KEY.STATE in data:
    if data[KEY.STATE] == 0 or data[KEY.STATE] == 1:
      sql += " and state = %d"%data[KEY.STATE]
  if KEY.TYPE in data:
    if data[KEY.TYPE] >= 0 and data[KEY.TYPE] <= 2:
      sql += " and type = %d"%data[KEY.TYPE]
  if KEY.LAST_TIME in data:
    sql += " and last_time > \"" + data[KEY.LAST_TIME] + "\""
  sql += " order by last_time DESC"
  sql_result = dbhelper.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      event_id_list.append(each_id)

  return event_id_list


'''
get user's follow or support events.
@params includes user's id and type of user's state in event.
                 user's state 0 indicates follow, and 1 indicates support.
@return an array of result event ids.
'''
def get_join_event_list(data):
  event_id_list = []
  if KEY.ID not in data:
    return event_id_list
  sql = "select event_id from support_relation where supporter = %d"%data[KEY.ID]
  if KEY.TYPE in data:
    if data[KEY.TYPE] == 1 or data[KEY.TYPE] == 2:
      sql += " and type = %d"%data[KEY.TYPE]
  sql += " order by time DESC"
  sql_result = dbhelper.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      event_id_list.append(each_id)

  return event_id_list


'''
manage relation of user and event.
@params
@return
'''
def user_event_manage(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data:
    return False
  if KEY.OPERATION not in data:
    return False
  if data[KEY.OPERATION] < 0 or data[KEY.OPERATION] > 2:
    return False
  sql = "select launcher from event where id = %d"
  launcher_id = None
  try:
    sql_result = dbhelper.execute_fetchone(sql%(data[KEY.EVENT_ID]))
    if sql_result is not None:
      launcher_id = sql_result[0]
  except:
    pass
  if launcher_id is None:
    return False
  if data[KEY.OPERATION] == 0:
    sql = "delete from support_relation where event_id = %d and supporter = %d"%(data[KEY.EVENT_ID], data[KEY.ID])
  else:
    sql = "replace into support_relation (event_id, supportee, supporter, type, time) values (%d, %d, %d, %d, now())"%(data[KEY.EVENT_ID], launcher_id, data[KEY.ID], data[KEY.OPERATION])
  try:
    dbhelper.execute(sql)
  except:
    return False

  #
  # trust and reputation compute here.
  #
  return True


'''
add a new comment to a help event or a exist comment.
@params includes event_id, represents comment belongs to which event,
                 author, user's id, author of comment,
                 content, content of comment,
                 parent_author, a author of parent comment
@return new comment id if succeed,
        -1 otherwise.
'''
def add_comment(data):

  if KEY.ID not in data or KEY.EVENT_ID not in data:
    return -1
  if KEY.CONTENT not in data:
    return -1
  data[KEY.CONTENT] = MySQLdb.escape_string(data[KEY.CONTENT].encode("utf8"))
  if KEY.PARENT_AUTHOR not in data:
    sql = "insert into comment (event_id, author, content, time) values (%d, %d, '%s', now())"
    sql = sql%(data[KEY.EVENT_ID], data[KEY.ID], data[KEY.CONTENT])
  else:
    sql = "insert into comment (event_id, author, content, time, parent_author) values (%d, %d, '%s', now(), %d)"
    sql = sql%(data[KEY.EVENT_ID], data[KEY.ID], data[KEY.CONTENT], data[KEY.PARENT_AUTHOR])
  try:
    comment_id = dbhelper.insert(sql)
    return comment_id
  except:
    return -1


'''
remove a comment from a help event by author him/her self.
@params includes id, indicates author him/her self.
                 event_id, indicates which event the comment belongs to.
                 comment_id, indicates comment itself.
@return True if delete successfully,
        False if fails.
'''
def remove_comment(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data or KEY.COMMENT_ID not in data:
    return False
  sql = "delete from comment where id = %d and event_id = %d and author = %d"
  try:
    n = dbhelper.execute(sql%(data[KEY.COMMENT_ID], data[KEY.EVENT_ID], data[KEY.ID]))
    if n > 0:
      return True
    else:
      return False
  except:
    return False


'''
get comments of a help event.
@params event_id, id of the help event.
@return a list of comments. each comment contain all detail information.
'''
def get_comments(data):
  if KEY.EVENT_ID not in data:
    return None
  comment_list = []
  comment = {}
  sql = "select id from comment where event_id = %d order by time DESC"
  try:
    sql_result = dbhelper.execute_fetchall(sql%(data[KEY.EVENT_ID]))
    for each_result in sql_result:
      for each_id in each_result:
        comment = {}
        comment[KEY.COMMENT_ID] = each_id
        comment = get_comment_info(comment)
        if comment is not None:
          comment_list.append(comment)
    return comment_list
  except:
    return None


'''
get detail information of a comment.
@params includes comment_id, id of comment.
@return information of comment, includes id of comment,
                                         event_id, indicates which event belongs to,
                                         author_id, author's user id,
                                         author, nickname of author,
                                         content, main body of comment,
                                         time, add time of comment.
        None indicates a fail query. Maybe the chosen comment doesn't exist.
'''
def get_comment_info(data):
  if KEY.COMMENT_ID not in data:
    return None
  sql = "select event_id, author, content, time, parent_author from comment where id = %d"
  comment_info = None
  try:
    sql_result = dbhelper.execute_fetchone(sql%(data[KEY.COMMENT_ID]))
    if sql_result is not None:
      comment_info = {}
      comment_info[KEY.COMMENT_ID] = data[KEY.COMMENT_ID]
      comment_info[KEY.EVENT_ID] = sql_result[0]
      comment_info[KEY.AUTHOR_ID] = sql_result[1]
      comment_info[KEY.CONTENT] = sql_result[2]
      comment_info[KEY.TIME] = str(sql_result[3])
      comment_info[KEY.PARENT_AUTHOR_ID] = sql_result[4]
      comment_info[KEY.AUTHOR] = None
      comment_info[KEY.PARENT_AUTHOR] = None

      user = {}
      user[KEY.ID] = comment_info[KEY.AUTHOR_ID]
      user = get_user_information(user)
      if user is not None:
        comment_info[KEY.AUTHOR] = user[KEY.NICKNAME]
      user = {}
      user[KEY.ID] = comment_info[KEY.PARENT_AUTHOR_ID]
      user = get_user_information(user)
      if user is not None:
        comment_info[KEY.PARENT_AUTHOR] = user[KEY.NICKNAME]
  except:
    pass
  finally:
    return comment_info


'''
add a static relation between two users. The relation is single direction.
@params includes two users' id, one is called id, the other called user_id.
parameter type indicates type of static relation. two users in one direction could only have one type of relation.
                 type:  0 indicates family relation.
                        1 indicates geography relation.
                        2 indicates career, interest and general friend relation.
@return True if successfully adds.
        False otherwise.
'''
def add_static_relation(data):
  if KEY.ID not in data or KEY.USER_ID not in data or KEY.TYPE not in data:
    return False
  sql = "replace into static_relation (user_a, user_b, type, time) values (%d, %d, %d, now())"
  try:
    n = dbhelper.execute(sql%(data[KEY.ID], data[KEY.USER_ID], data[KEY.TYPE]))
    if n > 0:
      return True
    else:
      return False
  except:
    return False


'''
remove a static relation of two user.
@params includes two users' id, one is called id, the other called user_id.
@return True if successfully removes.
        False otherwise.
'''
def remove_static_relation(data):
  if KEY.ID not in data or KEY.USER_ID not in data:
    return False
  sql = "delete from static_relation where user_a = %d and user_b = %d"
  try:
    n = dbhelper.execute(sql%(data[KEY.ID], data[KEY.USER_ID]))
    if n > 0:
      return True
    else:
      return False
  except:
    return False


'''
give an evaluation to a user in a help event.
@params includes: id, evaluater.
                  user_id, evaluatee.
                  event_id, indicates the help event.
                  value, the value of evaluation.
@return True if successfully evaluate.
        Flase otherwise.
'''
def evaluate_user(data):
  if KEY.ID not in data or KEY.USER_ID not in data or KEY.EVENT_ID not in data:
    return False
  if KEY.VALUE not in data:
    return False

  value_list = ast.literal_eval(data[KEY.VALUE])
  value = 0.0
  for each_value in value_list:
    value += each_value
  list_len = len(value_list)
  if list_len == 0:
    list_len = 1
  value /= list_len

  sql = "replace into evaluation (event_id, from, to, value, time) values (%d, %d, %d, %f, now())"
  try:
    dbhelper.execute(sql%(data[KEY.EVENT_ID], data[KEY.ID], data[KEY.USER_ID], value))
    return True
  except:
    return False



'''
add a health record of a user into database.
@params includes id, user's id.
                 height, user's height.
                 weight, user's weight.
                 blood_type, user's blood type.
                 medicine_taken, medicine user used to have
                 medical_history, user's medical chart
                 anaphylaxis, user's allergic reaction
@return the health record id of the new record.
        -1 indicates fail.
'''
def health_record(data):
  if KEY.ID not in data:
    return -1
  sql = "insert into health (user_id, time) values (%d, now())"%data[KEY.ID]
  record_id = -1
  try:
    record_id = dbhelper.insert(sql)
    if record_id > 0:
      if not update_health_record(data):
        return -1
    return record_id
  except:
    record_id = -1
  finally:
    return record_id


'''
get details of one certain health record.
@params includes user_id, id of the user.
@return details of the health record, contains record id, user id, type, certain value and record time.
        None indicates fail query.
'''
def get_health_record(user_id):
  sql = "select * from health where user_id = %d"
  record = None
  try:
    sql_result = dbhelper.execute_fetchone(sql%(user_id))
    if sql_result is not None:
      record = {}
      record[KEY.HEALTH_ID] = sql_result[0]
      record[KEY.USER_ID] = sql_result[1]
      record[KEY.HEIGHT] = sql_result[2]
      record[KEY.WEIGHT] = sql_result[3]
      record[KEY.BLOOD_TYPE] = sql_result[4]
      record[KEY.MEDICINE_TAKEN] = sql_result[5]
      record[KEY.MEDICAL_HISTORY] = sql_result[6]
      record[KEY.ANAPHYLAXIS] = sql_result[7]
  except:
    record = None
  finally:
    return record


'''
---------------------change the database & this method is not used-----------------------
get all health records of a user, but at most 100 records.
@params includes id, user's id.
@return a list that contain all health records. each element is a json that contains details information of a health record.
        None indicates fail query.
def get_health_records(data):
  if KEY.ID not in data:
    return None
  sql = "select id from health where user_id = %d order by time DESC limit %d"
  sql_result = None
  try:
    sql_result = dbhelper.execute_fetchall(sql%(data[KEY.ID], 100))
  except:
    sql_result = None
  records = None
  if sql_result is not None:
    records = []
    for each_result in sql_result:
      for each_id in each_result:
        a_record = get_health_record(each_id)
        if a_record is not None:
          records.append(a_record)
  return records
-----------------------------------------------------------------------------------------
'''


'''
add an illness record of a user into database.
@params includes id, user's id.
                 content, illness detail information.
@return illness record id.
        -1 indicates fail.
'''
def illness_record(data):
  if KEY.ID not in data or KEY.CONTENT not in data:
    return -1
  sql = "insert into illness (user_id, content, time) values (%d, '%s', now())"
  illness_id = -1
  try:
    illness_id = dbhelper.insert(sql%(data[KEY.ID], data[KEY.CONTENT]))
  except:
    illness_id = -1
  finally:
    return illness_id


'''
get details of an illness record.
@params includes record id, indicates which record to be queried.
@return content of an illness record, includes record's id, user's id, illness content and illness time.
        None indicates fail query or no such record.
'''
def get_illness_record(record_id):
  sql = "select id, user_id, content, time from illness where id = %d"
  record = None
  try:
    sql_result = dbhelper.execute_fetchone(sql%(record_id))
    if sql_result is not None:
      record = {}
      record[KEY.ILLNESS_ID] = sql_result[0]
      record[KEY.USER_ID] = sql_result[1]
      record[KEY.CONTENT] = sql_result[2]
      record[KEY.TIME] = str(sql_result[3])
  except:
    record = None
  finally:
    return record


'''
get all illness records of a user, but at most 100 records.
@params includes: id, user's id.
@return a list that contain all illness records. each element in the list is a json that is consist of details of an illness record.
        None indicates fail query.
'''
def get_illness_records(data):
  if KEY.ID not in data:
    return None
  sql = "select id from illness where user_id = %d order by time ASC limit %d"
  sql_result = None
  records = None
  try:
    sql_result = dbhelper.execute_fetchall(sql%(data[KEY.ID], 100))
  except:
    sql_result = None
  if sql_result is not None:
    records = []
    for each_result in sql_result:
      for each_id in each_result:
        a_record = get_illness_record(each_id)
        if a_record is not None:
          records.append(a_record)
  return records


'''
create a loving bank account. It contains loving bank and credit.
@params includes user_id, user's id, initial coin number and initial score value.
@return new bank account id if succeed.
        -1 if fail.
'''
def create_loving_bank(data, init_coin=0, init_score=0):
  if KEY.ID not in data:
    return -1
  sql = "insert into loving_bank (userid, love_coin, score_rank, score_exchange) values (%d, %d, %d, %d)"
  try:
    bank_account_id = dbhelper.insert(sql%(data[KEY.ID], init_coin, init_score, init_score))
    return bank_account_id
  except:
    return -1


'''
user could sign in once a day. Especially, if user has signed in today, this method would return false.
@params includes user_id. user's id.
@return True if sign in successfully.
        False otherwise.
'''
def sign_in(data):
  if KEY.ID not in data:
    return False
  user_id = data[KEY.ID]
  if is_sign_in(user_id):
    return False
  sql = "insert into sign_in (user_id, time) values (%d, now())"
  try:
    sign_in_id = dbhelper.insert(sql%(data[KEY.ID]))
    if sign_in_id > 0:
      add_score = {}
      add_score[KEY.ID] = user_id
      add_score[KEY.OPERATION] = 0
      add_score[KEY.LOVE_COIN] = 0
      add_score[KEY.SCORE] = 100
      if update_loving_bank(add_score):
        return True
      else:
        return False
    else:
      return False
  except:
    return False


'''
check whether a user has signed in today.
@params includes user_id. user's id.
@return True if user has signed in.
        False otherwise.
'''
def is_sign_in(user_id):
  result = False
  date_format = "\%Y-\%M-\%D \%H:\%i"
  sql = "select count(*) from sign_in where user_id = %d and to_days(time) = to_days(now())"%(user_id)
  # sql = "select count(*) from sign_in where user_id = %d and date_format(time, '%s') = date_format(now(), '%s')"%(user_id, date_format, date_format)
  try:
    sql_result = dbhelper.execute_fetchone(sql)[0]
    if sql_result > 0:
      result = True
    else:
      result = False
  except:
    result = False
  finally:
    return result

'''
get user's neighbors
@param includes: user_id, user's id
       options:  type, in data, indicates get a list of all user's information
                       not in data, get the identity ids list
@return
'''
def get_neighbor(data):
  neighbor_uid_list = []
  if KEY.ID not in data:
    return neighbor_uid_list
  user = get_user_information(data)
  if user is None:
    return neighbor_uid_list
  DISTANCE = 25.0 # 25000m
  location_range = haversine.get_range(user[KEY.LONGITUDE], user[KEY.LATITUDE], DISTANCE)
  sql = "select id from user where " \
        "longitude > %f and longitude < %f " \
        "and latitude > %f and latitude < %f"
  sql_result = dbhelper.execute_fetchall(
    sql%(location_range[0], location_range[1], location_range[2], location_range[3]))

  if KEY.TYPE in data:
    for each_result in sql_result:
      user = {}
      user[KEY.ID] = each_result[0]
      user = get_user_information(user)
      if user is not None:
        neighbor_uid_list.append(user)
  else:
    for each_result in sql_result:
      user = {}
      user[KEY.ID] = each_result[0]
      user = get_user_information(user)
      if user is not None:
        neighbor_uid_list.append(user[KEY.IDENTITY_ID])
  return neighbor_uid_list

'''
get help_events happend around the user
@param include event id
 option params includes state indicates all events or those starting or ended.
                        type indicates type of events.
                        state indicates state of events.
                        last_time indicates the last time client update.
@return a list of event
'''
def get_nearby_event(data):
  nearby_event_list = []
  if KEY.ID not in data:
    return nearby_event_list
  user = get_user_information(data)
  DISTANCE = 25.0 # 25000m
  location_range = haversine.get_range(user[KEY.LONGITUDE], user[KEY.LATITUDE], DISTANCE)
  sql = "select id from event where " \
        "longitude > %f and longitude < %f " \
        "and latitude > %f and latitude < %f"\
        %(location_range[0], location_range[1], location_range[2], location_range[3])
  if KEY.TYPE in data:
    sql += " and type = %d"%data[KEY.TYPE]
  if KEY.STATE in data:
    sql += " and state = %d"%data[KEY.STATE]
  if KEY.LAST_TIME in data:
    sql += " and last_time > '%s'"%data[KEY.LAST_TIME]
  sql += " order by time DESC"
  sql_result = dbhelper.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      nearby_event_list.append(each_id)
  return nearby_event_list


'''
get information about loving_bank
@param user_id, user's id
@return user's love coin and score
'''
def get_user_loving_bank(data):
  if KEY.USER_ID not in data:
    return None
  sql = "select score_rank, love_coin from loving_bank where userid = %d"
  try:
    res = dbhelper.execute_fetchone(sql%(data[KEY.USER_ID]))
    if res is None:
      return None
    else:
      bank_info = {}
      bank_info[KEY.ID] = data[KEY.USER_ID]
      bank_info[KEY.SCORE] = res[0]
      bank_info[KEY.LOVE_COIN] = res[1]
      return bank_info
  except:
    return None


'''
add an answer to a question
@param  data contains author_id, event_id, content
@return answer_id if successfully adds
    -1 is fails.
'''
def add_answer(data):
  if KEY.AUTHOR_ID not in data or KEY.EVENT_ID not in data or KEY.CONTENT not in data:
    return -1
  sql = "insert into answer (event_id, author_id) values (%d, %d)"
  answer_id = -1
  try:
    answer_id = dbhelper.insert(sql%(data[KEY.EVENT_ID], data[KEY.AUTHOR_ID]))
    if answer_id > 0:
      data[KEY.ANSWER_ID] = answer_id
      update_answer(data)
      event = {}
      event[KEY.ID] = data[KEY.AUTHOR_ID]
      event[KEY.EVENT_ID] = data[KEY.EVENT_ID]
      event[KEY.OPERATION] = 1
      if user_event_manage(event) is False:
        return -1
    return answer_id
  except:
    return -1


'''
update information about an answer
@param
@return
'''
def update_answer(data):
  if KEY.ANSWER_ID not in data:
    return False

  sql = "select author_id, event_id from answer where id = %d"%data[KEY.ANSWER_ID]
  try:
    res = dbhelper.execute_fetchone(sql)
    if res is None:
      return False
    author_id = res[0]
    event_id = res[1]

  except:
    return False

  result = True
  sql = ""
  if KEY.CONTENT in data:
    data[KEY.CONTENT] = MySQLdb.escape_string(data[KEY.CONTENT].encode("utf8"))
    sql = "update answer set content = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.CONTENT], data[KEY.ANSWER_ID]))
      result &= True
    except:
      result &= False
  if KEY.IS_ADOPTED in data:
    sql = "update answer set is_adopted = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.IS_ADOPTED], data[KEY.ANSWER_ID]))
      result &= True

      event = {}
      event[KEY.ID] = author_id
      event[KEY.EVENT_ID] = event_id
      event[KEY.OPERATION] = 2
      result &= user_event_manage(event)
    except:
      result &= False
  if KEY.LIKING_NUM in data:
    sql = "update answer set liking_num = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LIKING_NUM], data[KEY.ANSWER_ID]))
      result &= True
    except:
      result &= False

  return result
'''
get information about an answer
@param data contains answer_id
@return concrete information about answer
    which contains id, event_id, author_id, content, time, is_adopted, liking_num.
'''
def get_answer_info(data):
  if KEY.ANSWER_ID not in data:
    return None
  answer_info = None
  sql = "select * from answer where id = %d"
  try:
    sql_result = dbhelper.execute_fetchone(sql%(data[KEY.ANSWER_ID]))
    if sql_result is not None:
      answer_info = {}
      answer_info[KEY.ID] = sql_result[0]
      answer_info[KEY.EVENT_ID] = sql_result[1]
      answer_info[KEY.AUTHOR_ID] = sql_result[2]
      answer_info[KEY.CONTENT] = sql_result[3]
      answer_info[KEY.TIME] = str(sql_result[4])
      answer_info[KEY.IS_ADOPTED] = sql_result[5]
      answer_info[KEY.LIKING_NUM] = sql_result[6]
  except:
    pass
  finally:
    return answer_info


'''
get a list of answer of the question
@param include event's id
@return a array of answers. each element is information of an answer
'''
def get_answers(data, get_answerid_list):
  answer_id_list = get_answerid_list(data)
  answer_list = []
  answer_info = {}
  for answer_id in answer_id_list:
    answer_info[KEY.ANSWER_ID] = answer_id
    answer_info = get_answer_info(answer_info)
    if answer_info is not None:
      answer_list.append(answer_info)
  return answer_list


'''
get the id list of a question
@param include event's id
@return a list of answer_id about the question
'''
def get_answer_id_list(data):
  answer_id_list = []
  if KEY.EVENT_ID not in data:
    return answer_id_list
  sql = "select id from answer where event_id = %d"%data[KEY.EVENT_ID]
  sql_result = dbhelper.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      answer_id_list.append(each_id)

  return answer_id_list

'''
query all the users whom the user follows/follows the user.
@params includes: user's id.
                  type indicates type of static relation. two users in one direction could only have one type of relation.
                  type: 0 indicates family relation.
                        1 indicates geography relation.
                        2 indicates career, interest and general friend relation.
                  state indicates the follow relation.
                  state: 0, query user's followed users
                         1, query user's follower
@return a list contains ids
        -1 if fails
'''
def query_follow(data):
  if KEY.ID not in data or KEY.STATE not in data:
    return -1
  if data[KEY.STATE] == 0:
    sql = "select user_b from static_relation where user_a = %d"%data[KEY.ID]
  elif data[KEY.STATE] == 1:
    sql = "select user_a from static_relation where user_b = %d"%data[KEY.ID]
  else:
    return -1

  user_list = []
  if KEY.TYPE in data:
    if data[KEY.TYPE] == 0 or data[KEY.TYPE] ==1 or data[KEY.TYPE] == 2:
      sql += " and type = %d"%data[KEY.TYPE]
  sql_result = dbhelper.execute_fetchall(sql)
  resp = {}
  for each_result in sql_result:
    for each_id in each_result:
      resp[KEY.ID] = each_id
      resp = get_user_information(resp)
      user_list.append(resp)
  return user_list

'''
get supporters for an event
@param includes event id
       options  type of supporters
@return a list of supporters
'''
def get_supporters(data):
  sup_list = []
  if KEY.EVENT_ID not in data:
    return sup_list
  sql = "select supporter from support_relation where event_id = %d"%data[KEY.EVENT_ID]
  if KEY.TYPE in data:
    sql += " and type = %d"%data[KEY.TYPE]
  sql_result = dbhelper.execute_fetchall(sql)
  resp = {}
  for each_result in sql_result:
    for each_id in each_result:
      resp[KEY.ID] = each_id
      resp = get_user_information(resp)
      sup_list.append(resp)
  return sup_list

'''
modify information of a health record.
@params  includes: id, user's id.
         options:  height, weight, blood_type,
                   medicine_taken, medical_history, anaphylaxis
@return True if successfully modifies.
        False otherwise.
'''
def update_health_record(data):
  result = True
  if KEY.ID not in data:
    return False
  sql = ""

  if KEY.HEIGHT in data:
    sql = "update health set height = %d where user_id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.HEIGHT], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.WEIGHT in data:
    sql = "update health set weight = %d where user_id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.WEIGHT], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.BLOOD_TYPE in data:
    data[KEY.BLOOD_TYPE] = MySQLdb.escape_string(data[KEY.BLOOD_TYPE].encode("utf8"))
    sql = "update health set blood_type = '%s' where user_id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.BLOOD_TYPE], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.MEDICINE_TAKEN in data:
    data[KEY.MEDICINE_TAKEN] = MySQLdb.escape_string(data[KEY.MEDICINE_TAKEN].encode("utf8"))
    sql = "update health set medicine_taken = '%s' where user_id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.MEDICINE_TAKEN], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.MEDICAL_HISTORY in data:
    data[KEY.MEDICAL_HISTORY] = MySQLdb.escape_string(data[KEY.MEDICAL_HISTORY].encode("utf8"))
    sql = "update health set medical_history = '%s' where user_id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.MEDICAL_HISTORY], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.ANAPHYLAXIS in data:
    data[KEY.ANAPHYLAXIS] = MySQLdb.escape_string(data[KEY.ANAPHYLAXIS].encode("utf8"))
    sql = "update health set anaphylaxis = '%s' where user_id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.ANAPHYLAXIS], data[KEY.ID]))
      result &= True
    except:
      result &= False

  return result

'''
judge the health_card is in database or not.
if it exist in database, update data.
else, insert data.
@param include: id, user's id
       options: height, weight, blood_type,
                medicine_taken, medical_history, anaphylaxis
@return True if insert or update successfully
        False if fail
'''
def upload_health(data):
  if KEY.ID not in data:
    return False
  sql = "select * from health where user_id = %d"%data[KEY.ID]
  res = dbhelper.execute_fetchone(sql)
  if res is not None:
    return update_health_record(data)
  else:
    if health_record(data) > 0:
      return True
  return False

'''
update information of user's loving bank.
@params  includes: id, user's id.
                   operation, 0 indicates add love_coin & score
                              1 indicates minus love_coin & score
                              2 indicates transform score to love_coin
                   love_coin, the number of love_coin to add/minus
                   score, the score number to add/minus
                   (the switch score must be the multiple of 100)
@return True if successfully update.
        False otherwise.
'''
def update_loving_bank(data):
  if KEY.ID not in data or KEY.OPERATION not in data:
    return False
  if KEY.LOVE_COIN not in data or KEY.SCORE not in data:
    return False

  user = {}
  user[KEY.USER_ID] = data[KEY.ID]
  bank_info = get_user_loving_bank(user)
  if bank_info is None:
    return False

  exchange_rate = 0.01
  if data[KEY.OPERATION] == 0:
    update_love_coin = bank_info[KEY.LOVE_COIN] + data[KEY.LOVE_COIN]
    update_score = bank_info[KEY.SCORE] + data[KEY.SCORE]
  elif data[KEY.OPERATION] == 1:
    update_love_coin = bank_info[KEY.LOVE_COIN] - data[KEY.LOVE_COIN]
    update_score = bank_info[KEY.SCORE] - data[KEY.SCORE]
  elif data[KEY.OPERATION] == 2:
    if data[KEY.SCORE] % 100 != 0:
      return False
    update_love_coin = bank_info[KEY.LOVE_COIN] + data[KEY.SCORE] * exchange_rate
    update_score = bank_info[KEY.SCORE] - data[KEY.SCORE]
  else:
    return False

  if update_love_coin < 0 or update_score < 0:
    return False

  sql = "update loving_bank set love_coin = %d, score_rank = %d where userid = %d"
  try:
    dbhelper.execute(sql%(update_love_coin, update_score, data[KEY.ID]))
    return True
  except:
    return False

'''
user_A transfer the love_coin to user_B
@param includes: sender: user_A's id, who want to transfer the love_coin
                 receiver: user_B's id, who receives the transferred love_coin
                 love_coin: the number of love_coin which would be transferred
@return True if transfer successfully
        False if fails
'''
def love_coin_transfer(data):
  if KEY.SENDER not in data or KEY.RECEIVER not in data:
    return False
  if KEY.LOVE_COIN not in data:
    return False

  sender = {}
  receiver = {}
  sender[KEY.USER_ID] = data[KEY.SENDER]
  receiver[KEY.USER_ID] = data[KEY.RECEIVER]
  sender = get_user_loving_bank(sender)
  receiver = get_user_loving_bank(receiver)

  if sender is None or receiver is None:
    return False
  update_sender_coin = sender[KEY.LOVE_COIN] - data[KEY.LOVE_COIN]
  update_receiver_coin = receiver[KEY.LOVE_COIN] + data[KEY.LOVE_COIN]

  if update_sender_coin < 0 or update_receiver_coin < 0:
    return False

  sql = "update loving_bank set love_coin = %d where userid = %d"
  history_sql = "insert into coin_exchange (sender, receiver, time, lovecoin) values (%d, %d, now(), %d)"
  try:
    dbhelper.execute(sql%(update_sender_coin, data[KEY.SENDER]))
    dbhelper.execute(sql%(update_receiver_coin, data[KEY.RECEIVER]))
    dbhelper.insert(history_sql%(data[KEY.SENDER], data[KEY.RECEIVER], data[KEY.LOVE_COIN]))
    return True
  except Exception, e:
    traceback.print_exc()
    return False


'''
get chat_token of an account.
@params include user's id.
@return chat_token of an account.
        None if account not exists or database query error.
'''
def get_chat_token(data):
  if KEY.ID not in data:
    return None
  sql = "select chat_token from account where id = '%s'"
  try:
    res = dbhelper.execute_fetchone(sql%(data[KEY.ID]))
    if res is None:
      return None
    else:
      return res[0]
  except:
    return None

'''
get the relation between two users(one-sided relation)
@param includes: id, user_a's id
                 user_id, user_b's id
@return 0 indicates families
        2 indicates friends
        -1 query fails
        others indicate no relation
'''
def get_relation(data):
  if KEY.ID not in data or KEY.USER_ID not in data:
    return -1
  sql = "select type from static_relation where user_a = %d and user_b = %d"
  try:
    res = dbhelper.execute_fetchone(sql%(data[KEY.ID], data[KEY.USER_ID]))
    if res is None:
      return -1
    else:
      return res[0]
  except:
    return -1

'''
save rewarding love_coin in the exchanged pool
@param includes: id, user's id
                 love_coin, the rewarding love_coin
@return True if saves successfully
        False if fails
'''
def exchange(data):
  if KEY.ID not in data or KEY.LOVE_COIN not in data:
    return False
  coin_sql = "select love_coin from loving_bank where userid = %d"%data[KEY.ID]
  exchange_sql = "select score_exchange from loving_bank where userid = %d"%data[KEY.ID]
  try:
    coin = dbhelper.execute_fetchone(coin_sql)
    coin_exchange = dbhelper.execute_fetchone(exchange_sql)
    if coin is None or coin_exchange is None:
      return False
    update_love_coin = coin[0] - data[KEY.LOVE_COIN]
    update_exchange_coin = coin_exchange[0] + data[KEY.LOVE_COIN]
    if update_love_coin < 0:
      return False

    update_sql = "update loving_bank set love_coin = %d, score_exchange = %d where userid = %d"
    dbhelper.execute(update_sql%(update_love_coin, update_exchange_coin, data[KEY.ID]))
  except:
    return False

'''
get a history record of a transfer
@param id, transfer_record's id
@return record information
        None if fails
'''
def get_transfer(data):
  record_info = None
  if KEY.ID not in data:
    return record_info
  sql = "select * from coin_exchange where id = %d"
  try:
    sql_result = dbhelper.execute_fetchone(sql%(data[KEY.ID]))
    if sql_result is not None:
      record_info = {}
      record_info[KEY.ID] = sql_result[0]
      record_info[KEY.SENDER] = sql_result[1]
      record_info[KEY.RECEIVER] = sql_result[2]
      record_info[KEY.LOVE_COIN] = sql_result[3]
      record_info[KEY.TIME] = str(sql_result[4])
    return record_info
  except:
    return None

'''
check the history of the transfer
@param  id, user's id
        type, 0 indicates send coins
              1 indicates receive coins
@return h_list, a list of transfer history
        -1 if query fails
'''
def check_transfer(data):
  if KEY.ID not in data or KEY.TYPE not in data:
    return -1
  sql = ""
  if data[KEY.TYPE] == 0:
    sql = "select id from coin_exchange where sender = %d"%data[KEY.ID]
  elif data[KEY.TYPE] == 1:
    sql = "select id from coin_exchange where receiver = %d"%data[KEY.ID]
  else:
    return -1
  sql += " order by time DESC"
  sql_result = dbhelper.execute_fetchall(sql)
  h_list = []
  for each_result in sql_result:
    for each_id in each_result:
      record = {}
      record[KEY.ID] = each_id
      record = get_transfer(record)
      if record is not None:
        h_list.append(record)
  return h_list


'''
reward the love_coin to the supporters when the event stops
@param includes: event_id, event's id
@return True if succeed
        False if fails
'''
def reward(data):
  if KEY.EVENT_ID not in data:
    return False
  event = get_event_information(data)
  if event == None:
    return False
  reward_coin = event[KEY.LOVE_COIN]
  if reward_coin is None:
    return False


  sup_event = {}
  sup_event[KEY.EVENT_ID] = data[KEY.EVENT_ID]
  sup_event[KEY.TYPE] = 2
  supporters = get_supporters(sup_event)
  if supporters is None:
    return False
  num = len(supporters)


  minus_sql = "update loving_bank set score_exchange = score_exchange - %d where userid = %d"
  try:
    userid = event[KEY.LAUNCHER_ID]
    if userid is None:
      return False
    dbhelper.execute(minus_sql%(reward_coin, userid))
  except Exception, e:
    return False

  add_sql = "update loving_bank set love_coin = love_coin + %d where userid = %d"
  history_sql = "insert into coin_trade (eventid, sender, receiver, lovecoin, time) " \
                "values (%d, %d, %d, %d, now())"
  if num == 0:
    try:
      dbhelper.execute(add_sql%(reward_coin, event[KEY.LAUNCHER_ID]))
      dbhelper.insert(history_sql%(data[KEY.EVENT_ID], event[KEY.LAUNCHER_ID], event[KEY.LAUNCHER_ID], reward_coin))
      return True
    except:
      return False
  else:
    # todo If the avg_coin less than 1(which will be zero).
    avg_coin = reward_coin / num;
    try:
      for i in range(0, num):
        dbhelper.execute(add_sql%(avg_coin, supporters[i][KEY.ID]))
        dbhelper.insert(history_sql%(data[KEY.EVENT_ID], event[KEY.LAUNCHER_ID], supporters[i][KEY.ID], reward_coin))
      return True
    except Exception, e:
      print e
      return False

'''
get all events by type and state
@param includes: type, the type of events.
                 state, the state of events.
@return id_list, a list of event_id.
        -1 if fails.
'''
def get_all_events(data):
  if KEY.TYPE not in data or KEY.STATE not in data:
    return -1
  id_list = []
  sql = "select id from event where type = %d and state = %d"%(data[KEY.TYPE], data[KEY.STATE])
  sql += " order by time DESC"
  sql_result = dbhelper.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      id_list.append(each_id)
  return id_list

'''
get the history of coin trade
@param includes: sender, get the history as sender
                 receiver, get the history as receiver
@return h_list, a list of the history of coin trade
        -1, if fails
'''
def get_trade(data):
  if KEY.SENDER not in data and KEY.RECEIVER not in data:
    return -1
  sql = "select * from coin_trade where"
  if KEY.SENDER in data and KEY.RECEIVER in data:
    sql += " sender = %d or receiver = %d"%(data[KEY.SENDER], data[KEY.RECEIVER])
  elif KEY.SENDER in data:
    sql += " sender = %d"%data[KEY.SENDER]
  elif KEY.RECEIVER in data:
    sql += " receiver = %d"%data[KEY.RECEIVER]
  sql += " order by time DESC"

  h_list = []
  sql_result = dbhelper.execute_fetchall(sql)
  for each_result in sql_result:
    history = {}
    history[KEY.EVENT_ID] = each_result[1]
    history[KEY.SENDER] = each_result[2]
    history[KEY.RECEIVER] = each_result[3]
    history[KEY.LOVE_COIN] = each_result[4]
    history[KEY.TIME] = str(each_result[5])
    h_list.append(history)
  return h_list
