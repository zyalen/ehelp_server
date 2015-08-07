__author__ = 'thetruthmyg'

from tornado.web import RequestHandler
from tornado.escape import json_encode

from utils import KEY
from utils import STATUS

import re

img_pattern = re.compile(r'(\W|\w)*(.jpg)', re.S)
vid_pattern = re.compile(r'(\W|\w)*(.mp4)', re.S)
sou_pattern = re.compile(r'(\W|\w)*(.mp3)', re.S)

'''
upload avatar for the account
@params a text as avatar's name and a file
    which is a picture, video or sound.
'''
class UploadAvatar_Handler(RequestHandler):

  def post(self):

    myfile = self.request.files['avatar'][0]
    resp = {}

    filename = myfile['filename']
    index = filename.rfind('\\')
    if index != -1:
      filename = filename[index + 1:]
    # save different types of file
    if re.match(img_pattern, filename):
      # save image
      upload_path = "./static/avatar/" + filename
      resp[KEY.STATUS] = write_file(myfile, upload_path)
    elif re.match(vid_pattern, filename):
      # save video
      upload_path = "./static/video/" + filename
      resp[KEY.STATUS] = write_file(myfile, upload_path)
    elif re.match(sou_pattern, filename):
      # save sound
      upload_path = "./static/sound/" + filename
      resp[KEY.STATUS] = write_file(myfile, upload_path)
    else:
      resp[KEY.STATUS] = STATUS.ERROR

    self.write(json_encode(resp))


'''
write the file to static directory
@param includes: myfile, the file to write
                upload_path, the path where the file saved
@return STATUS.OK if write successfully
        STATUS.ERROR if fails
'''
def write_file(myfile, upload_path):
  try:
    fin = open(upload_path, "wb")
    fin.write(myfile["body"])
    fin.close()
    return STATUS.OK
  except:
    return STATUS.ERROR