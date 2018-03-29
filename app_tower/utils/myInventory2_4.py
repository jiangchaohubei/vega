#!/usr/bin/env python
# -*- coding:utf8 -*-
from ansible.inventory.manager import InventoryManager
from ansible.inventory.group import Group
from ansible.inventory.host import Host
import logging
log = logging.getLogger("tasks") # 为loggers中定义的名称

class myInventory(InventoryManager):
    """
    this is my ansible inventory object.
    """
    def __init__(self, resource, loader,sources=[]):
        """
        resource的数据格式是一个列表字典，比如
            {
                "group1": {
                    "hosts": [{"hostname": "10.0.0.0", "port": "22", "username": "test", "password": "pass"}, ...],
                    "vars": {"var1": value1, "var2": value2, ...}
                }
            }

        如果你只传入1个列表，这默认该列表内的所有主机属于default_group组,比如
            [{"hostname": "10.0.0.0", "port": "22", "username": "test", "password": "pass"}, ...]
        """
        self.resource = resource
        #     {
        #     u'test': {
        #         'hosts': [
        #             {'username': '', 'password': '','ip':u'113.209.107.36', 'hostname': u'113.209.107.36', 'port': '22'},
        #             {'username': '', 'password': '','ip':u'10.200.56.28', 'hostname': u'10.200.56.28', 'port': '22'}
        #         ],
        #         'vars': {'anisble_ssh_pass': 'z8xFC9l~', 'ansible_ssh_user': 'root'}
        #     }
        # }
        self.inventory = InventoryManager(loader=loader,  sources=sources)


    def my_add_group(self, hosts, groupname, groupvars=None):
        log.info( 'my_add_group')
        log.info( str(hosts))
        """
        add hosts to a group
        """

        self.inventory.add_group(groupname)
        for host in hosts:

            # set connection variables
            hostname = host.get("hostname")
            hostip = host.get('ip', hostname)
            hostport = host.get("port")
            username = host.get("username")
            password = host.get("password")
            #ssh_key = host.get("ssh_key")

            self.inventory.add_host(hostname,groupname)
            self.inventory.get_host(hostname).set_variable( 'ansible_ssh_host', hostip)
            self.inventory.get_host(hostname).set_variable('ansible_ssh_port', hostport)
            self.inventory.get_host(hostname).set_variable( 'ansible_ssh_user', username)
            self.inventory.get_host(hostname).set_variable( 'ansible_ssh_pass', password)
            for key, value in host.iteritems():
                if key not in ["hostname", "port",'ip', "username", "password"]:
                    self.inventory.get_host(hostname).set_variable(key, value)
            #加到all里面
            #self.inventory.get_groups_dict()['all'].add_host(my_host)




    def gen_inventory(self):
        log.info( 'gen_inventory')
        """
        add hosts to inventory.
        """
        if isinstance(self.resource, list):

            log.info( self.resource)
            self.my_add_group(self.resource, 'default_group')
        elif isinstance(self.resource, dict):

            log.info( self.resource)
            for groupname, hosts_and_vars in self.resource.iteritems():
                log.info( groupname+":"+str(hosts_and_vars.get("hosts")))
                self.my_add_group(hosts_and_vars.get("hosts"), 'all', hosts_and_vars.get("vars"))

    def get_inventory(self):
        log.info( 'get_inventory')
        self.gen_inventory()

        return self.inventory
