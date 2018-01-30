#!/usr/bin/env python
# -*- coding:utf8 -*-
import json
from channels import Group




def ws_connect(message):
    Group('users').add(message.reply_channel)
    Group('users').send({
        'text': json.dumps({
            'message': u'有用户连接',

        })
    })



def ws_disconnect(message):
    Group('users').send({
        'text': json.dumps({
            'message': u'有用户断开连接',
        })
    })
    Group('users').discard(message.reply_channel)