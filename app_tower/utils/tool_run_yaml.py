#!/usr/bin/env python
# -*- coding:utf8 -*-
'''
 ansible调用playbook
'''
import os
import json
from collections import namedtuple

from app_tower.utils.myInventory import myInventory

from ansible.vars import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.errors import AnsibleParserError

from ansible import constants as C

import logging
log = logging.getLogger("playbook_run") # 为loggers中定义的名称

class runyaml:
    def __init__(self, logfile,playbook_path,group,extra_vars={},tags=None,skip_tags=None,fork=5):
        log.info('runplaybook init')
        self.logfile=logfile
        self.playbook_path=playbook_path
        self.group=group
        self.extra_vars=extra_vars
        self.tags=tags
        self.skip_tags=skip_tags
        self.fork=fork
        log.info('group:'+str(self.group))

    def run(self):
        log.info('runplaybook run')
        play_book = my_ansible_play(self.logfile,self.playbook_path,self.group,extra_vars=self.extra_vars,tags=self.tags,skip_tags=self.skip_tags,fork=self.fork)
        #play_book = my_ansible_play(self.logfile,'/root/code/ping.yml')
        run_msg=play_book.run()
        if run_msg['code'] in [1001,1002,1003]:
            return run_msg
        log.info('runplaybook run'+str(play_book.get_result()))
        return play_book.get_result()


class mycallback(CallbackBase):
    # 这里是状态回调，各种成功失败的状态,里面的各种方法其实都是从写于CallbackBase父类里面的，其实还有很多，可以根据需要拿出来用
    def __init__(self,fo, *args):
        super(mycallback, self).__init__(display=None)
        self.status_ok = json.dumps({})
        self.status_fail = json.dumps({})
        self.status_unreachable = json.dumps({})
        self.status_playbook = ''
        self. status_no_hosts = False
        self.host_ok = {}
        self.host_failed = {}
        self.host_unreachable = {}
        self.host_skipped={}
        self.fo=fo
        self.recap = {}#概括


    def v2_runner_on_async_poll(self, result):
        log.info('v2_runner_on_async_poll')
        host = result._host.get_name()
        jid = result._result.get('ansible_job_id')
        #FIXME, get real clock
        clock = 0
        self.runner_on_async_poll(host, result._result, jid, clock)
        print 'v2_runner_on_async_poll'

    def v2_runner_on_async_ok(self, result):
        log.info('v2_runner_on_async_ok')
        host = result._host.get_name()
        jid = result._result.get('ansible_job_id')
        self.runner_on_async_ok(host, result._result, jid)
        print 'v2_runner_on_async_ok'

    def v2_runner_on_async_failed(self, result):
        log.info('v2_runner_on_async_failed')
        host = result._host.get_name()
        jid = result._result.get('ansible_job_id')
        self.runner_on_async_failed(host, result._result, jid)
        print 'v2_runner_on_async_failed'
    def v2_playbook_on_task_start(self, task, is_conditional):
        log.info('v2_playbook_on_task_start')
        self.playbook_on_task_start(task.name, is_conditional)
        print 'v2_playbook_on_task_start'
    def v2_playbook_on_setup(self):
        log.info('v2_playbook_on_setup')
        self.playbook_on_setup()
        print 'v2_playbook_on_setup'
    def v2_playbook_on_import_for_host(self, result, imported_file):
        log.info('v2_playbook_on_import_for_host')
        host = result._host.get_name()
        self.playbook_on_import_for_host(host, imported_file)
        print 'v2_playbook_on_import_for_host'

    def v2_playbook_on_not_import_for_host(self, result, missing_file):
        log.info('v2_playbook_on_not_import_for_host')
        host = result._host.get_name()
        self.playbook_on_not_import_for_host(host, missing_file)
        print 'v2_playbook_on_not_import_for_host'
    def v2_on_file_diff(self, result):
        log.info('v2_on_file_diff')
        if 'diff' in result._result:
            host = result._host.get_name()
            self.on_file_diff(host, result._result['diff'])
            print 'v2_on_file_diff'




    def v2_runner_on_skipped(self, result):
        log.info('v2_runner_on_skipped')
        if C.DISPLAY_SKIPPED_HOSTS:
            host = result._host.get_name()
            self.runner_on_skipped(host, self._get_item(getattr(result._result,'results',{})))
            self.host_skipped[host] = result
            print result._result['msg']
            self.fo.writelines('skipped['+host+']*****************************************************************************************************************'+'\n')
            self.fo.writelines('skipped:'+host+'=>'+json.dumps(result._result,sort_keys=True,indent=8)+'\n')
            self.fo.flush()
            log.info('v2_runner_on_skipped: host'+host+' msg :'+str(result._result))
            print 'v2_runner_on_skipped'
    def v2_runner_on_ok(self, result):
        log.info('v2_runner_on_ok')
        host = result._host.get_name()
        self.runner_on_ok(host, result._result)
        # self.status_ok=json.dumps({host:result._result},indent=4)
        self.host_ok[host] = result
        self.fo.writelines('ok['+host+']*****************************************************************************************************************'+'\n')

        print 'okokok',result._result
        self.fo.writelines( 'ok'+host+'=>'+json.dumps(result._result,sort_keys=True,indent=8)+'\n')
        self.fo.flush()
        log.info('v2_runner_on_ok :'+str(result._result))
        # for i in result._result.keys():
        #      self.fo.writelines( i+'=>'+str(result._result[i]))


    def v2_runner_on_failed(self, result, ignore_errors=False):
        log.info('v2_runner_on_failed')
        host = result._host.get_name()
        self.runner_on_failed(host, result._result, ignore_errors)
        # self.status_fail=json.dumps({host:result._result},indent=4)
        self.host_failed[host] = result
        self.fo.writelines('failed['+host+']*****************************************************************************************************************'+'\n')
        self.fo.writelines('failed:'+host+'=>'+json.dumps(result._result,sort_keys=True,indent=8)+'\n')
        self.fo.flush()
        log.info('v2_runner_on_failed: host'+host+' msg :'+str(result._result))

    def v2_runner_on_unreachable(self, result):
        log.info('v2_runner_on_unreachable')
        host = result._host.get_name()
        self.runner_on_unreachable(host, result._result)
        # self.status_unreachable=json.dumps({host:result._result},indent=4)
        self.host_unreachable[host] = result
        self.fo.writelines('unreachable['+host+']*****************************************************************************************************************'+'\n')
        self.fo.writelines('unreachable:'+host+'=>'+json.dumps(result._result,sort_keys=True,indent=8)+'\n')
        self.fo.flush()
        log.info('v2_runner_on_unreachable:host'+host+' msg :'+str(result._result))

    def v2_playbook_on_no_hosts_matched(self):
        log.info('v2_playbook_on_no_hosts_matched')
        self.playbook_on_no_hosts_matched()
        self.status_no_hosts = True

        self.fo.writelines('no hosts matched'+'\n')
        self.fo.flush()

    def v2_playbook_on_play_start(self, play):
        log.info('v2_playbook_on_play_start :'+play.name)
        self.playbook_on_play_start(play.name)
        self.playbook_path = play.name
        self.fo.writelines('PLAY ['+play.name+'] *****************************************************************************************************************'+'\n')
        self.fo.writelines('TASK [Gathering Facts] **************************************************************************************************************'+'\n')
        self.fo.flush()
    def v2_playbook_on_stats(self, stats):
        log.info('v2_playbook_on_stats ')
        self.playbook_on_stats(stats)
        hosts = sorted(stats.processed.keys())
        myrecap=""
        for h in hosts:
            t = stats.summarize(h)

            msg = "PLAY RECAP [%s] : %s %s %s %s %s" % (
                h,
                "ok: %s" % (t['ok']),
                "changed:%s" % (t['changed']),
                "unreachable: %s" % (t['unreachable']),
                "skipped: %s" % (t['skipped']),
                "failed: %s" % (t['failures']),
            )
            self.recap[h]={'ok':t['ok'],'changed':t['changed'],'unreachable':t['unreachable'],'skipped':t['skipped'],'failed':t['failures']}
            myrecap+=msg+'\n'
            print 'RECAP>>>',msg
        log.info('v2_playbook_on_stats :'+myrecap)
        self.fo.writelines("PLAY RECAP*****************************************************************************************************************"+'\n')
        self.fo.writelines(myrecap+'\n')
        self.fo.flush()

class my_ansible_play():
    # 这里是ansible运行
    # 初始化各项参数，大部分都定义好，只有几个参数是必须要传入的
    def __init__(self,logfile, playbook,group, extra_vars={},
                 host_list='/etc/ansible/hosts',
                 connection='ssh',
                 become=False,
                 become_user=None,
                 module_path=None,
                 fork=50,
                 ansible_cfg=None,  # os.environ["ANSIBLE_CONFIG"] = None
                 passwords={},
                 check=False,
                 tags=None,
                 skip_tags=None,
                 ):
        self.logfile=logfile
        self.playbook_path = playbook
        self.passwords = dict(conn_pass='AAA')
        self.extra_vars = extra_vars
        Options = namedtuple('Options',
                             ['connection',
                              'remote_user',
                              'ask_sudo_pass',
                              'verbosity',
                              'ack_pass',
                              'module_path',
                              'forks',
                              'become',
                              'become_method',
                              'become_user',
                              'check',
                              'listhosts',
                              'listtasks',
                              'listtags',
                              'syntax',
                              'sudo_user',
                              'sudo',
                              'tags',
                              'skip_tags',
                              'ssh_extra_args',
                              ])
        self.options = Options(connection='smart',
                               remote_user='root',
                               ask_sudo_pass=False,
                               verbosity=5,
                               ack_pass=None,
                               module_path=None,
                               forks=fork,
                               become=False,
                               become_method=None,
                               become_user=None,
                               check=check,
                               listhosts=None,
                               listtasks=None,
                               listtags=None,
                               syntax=None,
                               sudo_user=None,
                               sudo=None,
                               tags=tags,
                               skip_tags=skip_tags,
                               ssh_extra_args=None,
                               )
        if ansible_cfg != None:
            os.environ["ANSIBLE_CONFIG"] = ansible_cfg
        self.variable_manager = VariableManager()
        self.loader = DataLoader()

        self.inventory=myInventory(resource=group,loader=self.loader, variable_manager=self.variable_manager, host_list=[]).get_inventory()
        #self.inventory = Inventory(loader=self.loader, variable_manager=self.variable_manager, host_list=host_list)

        self.variable_manager.set_inventory(self.inventory)

        self.variable_manager.extra_vars=self.extra_vars


    # 定义运行的方法和返回值
    def run(self):
        log.info('run')
        fo = open(self.logfile, "r+")
        complex_msg = {}
        if not os.path.exists(self.playbook_path):
            code = 1001
            results = {'playbook': self.playbook_path, 'msg': self.playbook_path + ' playbook is not exist',
                       'flag': False}
            complex_msg['code']=code
            complex_msg['results']=results
            fo.writelines('[ERROR]>>>>>'+results['msg']+'\n')
            fo.flush()
            fo.close()
            log.error('error:'+str(results))
            return complex_msg
            # results=self.playbook_path+'playbook is not existed'
            # return code,complex_msg,results

        pbex = PlaybookExecutor(playbooks=[self.playbook_path],
                                inventory=self.inventory,
                                variable_manager=self.variable_manager,
                                loader=self.loader,
                                options=self.options,
                                passwords=self.passwords)

        self.results_callback = mycallback(fo)
        pbex._tqm._stdout_callback = self.results_callback
        try:
            log.info('run start')
            code = pbex.run()
            log.info('run end')
            print code
        except AnsibleParserError:
            code = 1002
            results = {'playbook': self.playbook_path, 'msg': self.playbook_path + ' playbook have syntax error',
                       'flag': False}
            complex_msg['code']=code
            complex_msg['results']=results
            fo.writelines('[ERROR]>>>>>'+results['msg']+'\n')
            fo.flush()
            fo.close()
            log.error('error:'+str(results))
            return complex_msg
        else:
            pass
        finally:
            pass

        if self.results_callback.status_no_hosts:
            code = 1003
            results = {'playbook': self.playbook_path, 'msg': self.results_callback.status_no_hosts, 'flag': False,
                       'executed': False}
            complex_msg['code']=code
            complex_msg['results']=results
            fo.close()
            log.error('error:'+str(results))
            return complex_msg

        complex_msg['code']=1000
        complex_msg['results']=''
        fo.close()
        log.info(str(complex_msg))
        return complex_msg
    def get_result(self):
        log.info('get_result start')
        self.result_all = {'code':1000,'recap':self.results_callback.recap,'no_host_matched':self.results_callback.status_no_hosts,'success': {}, 'fail': {}, 'unreachable': {},'skipped':{}}
        # print result_all
        # print dir(self.results_callback)
        for host, result in self.results_callback.host_ok.items():
            self.result_all['success'][host] = result._result

        for host, result in self.results_callback.host_failed.items():
            pass
            self.result_all['fail'][host] = result._result
        for host, result in self.results_callback.host_skipped.items():
            pass
            self.result_all['skipped'][host] = result._result
        for host, result in self.results_callback.host_unreachable.items():
            #self.result_all['unreachable'][host] = result._result['msg']
            self.result_all['unreachable'][host] = result._result

        for i in self.result_all['success'].keys():
            print i, self.result_all['success'][i]
        print self.result_all['fail']
        print self.result_all['unreachable']
        log.info('result: '+str(self.result_all))
        log.info('get_result end')
        return self.result_all


# if __name__ == '__main__':
#     play_book = my_ansible_play('/usr/local/code/user.yml')
#     play_book.run()
#     play_book.get_result()
