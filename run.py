#!/usr/env/python3
# -*- coding: UTF-8 -*-
import os
from passport.do_login import do_login
from passport.mess import get_current_time, set_logger

def main():
    set_logger(os.path.join('log', f'bupt_login_{get_current_time()}.log'))
    do_login()

if __name__ == '__main__':
    main()
