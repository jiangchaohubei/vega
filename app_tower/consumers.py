#!/usr/bin/env python
# -*- coding:utf8 -*-
import json
from channels import Group
from channels.auth import http_session


@http_session
def ws_connect(message):
    Group('User').add(message.reply_channel)
    if message.http_session['isAdministrant']:
        Group('Administrant').add(message.reply_channel)

    Group('User').send({
        'text': json.dumps({
            'message': u'用户[%s]登录' % message.http_session['username']

        })
    })



def ws_disconnect(message):

    Group('User').discard(message.reply_channel)

    Group('Administrant').discard(message.reply_channel)

    Group('User').send({
        'text': json.dumps({
            'message': u'用户[%s]注销' % message.http_session['username']

        })
    })
