# -*- coding: utf-8 -*-
# TODO: login to swu-net
# author=QIUKU

from swu_net import SwuNet

swu_net = SwuNet()
key = swu_net.ask_for_key()
session_id = swu_net.get_session_id()
swu_net.login(key=key, session_id=session_id)

