#!/usr/bin/env python
# -*- coding:utf8 -*-
import json
from channels import Group
from channels.auth import http_session
import logging
log = logging.getLogger("message")

@http_session
def ws_connect(message):
    log.info("ws_connect start")
    Group('User').add(message.reply_channel)
    if message.http_session['isAdministrant']:
        Group('Administrant').add(message.reply_channel)

    Group('User').send({
        'text': json.dumps({
            'message': u'用户[%s]登录' % message.http_session['username'],
            'type':'login'

        })
    })



def ws_disconnect(message):
    log.info("ws_disconnect start")

    Group('User').discard(message.reply_channel)

    Group('Administrant').discard(message.reply_channel)

    Group('User').send({
        'text': json.dumps({
            'message': u'用户注销',
            'type':'login'

        })
    })
