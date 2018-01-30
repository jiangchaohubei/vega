#!/usr/bin/env python
# -*- coding:utf8 -*-

from channels.routing import route
from app_tower.consumers import ws_connect, ws_disconnect


channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
]