#!/usr/python
# -*- coding: utf-8 -*-
from tornado.escape import json_decode



def decode_params(request):
  params = {}
  try:
    if request.headers.get("Content-Type") == "application/json":
      params = json_decode(request.body)
  except:
    pass
  finally:
    return params


