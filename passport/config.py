"""Configs of this app."""
#!/usr/env/python3
# -*- coding: UTF-8 -*-

try:
    from .credentials import *
except ImportError as credentials_import_error:
    print(credentials_import_error.args)
    raise ImportError("Failed to import credentials. Please make sure `credentials.py` exists.")

HTTP_CLIENT_MAX_RETRIES = 4
HTTP_CLIENT_TIME_OUT = 10
HTTP_CLIENT_REFERER = 'http://my.bupt.edu.cn/index.portal'
LOGIN_MAX_ATTEMPT = 3
LOGIN_WAIT_INTERVEL = 5
WEB_VPN_ALLOW_ERROR = True
