# -*- coding: utf-8 -*-
# TODO: login to swu-net
# author=QIUKU

from swu_net import SwuNet

swu_net = SwuNet()
key = swu_net.ask_for_key()
swu_net.exit(key=key)

