#!/usr/env/python3
# -*- coding: UTF-8 -*-
from .login_helper.login_helper import HTTPClient
from .login_helper.web_vpn_helper import WebVPNHelper
from .login_helper.auth_helper import AuthHelper

def do_login(session=None):
    """Send login requests.

    :param session: Attached Requests session.
    :type session: requests.Session.
    :return: Requests session.
    """
    http_client = HTTPClient(session) if session else HTTPClient()
    webvpn_helper = WebVPNHelper(http_client)
    auth_helper = AuthHelper(http_client)
    webvpn_helper.do_login(error_notice='Web VPN (webvpn.bupt.edu.cn)')
    auth_helper.do_login(error_notice='Auth (my.bupt.edu.cn)')
    return session

if __name__ == '__main__':
    do_login()
