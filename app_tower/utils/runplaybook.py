# /usr/bin/python2
# -*- coding: utf-8 -*
import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor

from app.models import jobTemplate

class runplaybook:
    def __init__(self, jobId):
        self.jobId = jobId
        job=jobTemplate.object.get(id=jobId)
        self.job=job

    def run(self):
        class ResultCallback(CallbackBase):
            """A sample callback plugin used for performing an action as results come in

            If you want to collect all results into a single object for processing at
            the end of the execution, look into utilizing the ``json`` callback plugin
            or writing your own custom callback plugin
            """

            def v2_runner_on_ok(self, result, **kwargs):
                """Print a json representation of the result

                This method could store the result in an instance attribute for retrieval later
                """
                host = result._host
                print json.dumps({host.name: result._result}, indent=4)


        results_callback = ResultCallback()

        # initialize needed objects
        variable_manager = VariableManager()
        loader = DataLoader()
        passwords = dict(conn_pass='AAA')

        # create inventory and pass to var manager
        inventory = Inventory(loader=loader, variable_manager=variable_manager)
        variable_manager.set_inventory(inventory)

        playbook_path = self.job.playbook
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
                              'sudo'])

        options = Options(connection='smart',
                          remote_user='root',
                          ack_pass=None,
                          sudo_user='root',
                          forks=5,
                          sudo='yes',
                          ask_sudo_pass=False,
                          verbosity=5,
                          module_path=None,
                          become=True,
                          become_method='sudo',
                          become_user='root',
                          check=None,
                          listhosts=None,
                          listtasks=None,
                          listtags=None,
                          syntax=None)
        pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,
                                loader=loader, options=options, passwords=passwords)
        pbex._tqm._stdout_callback = results_callback
        results = pbex.run()
        return results
