# vim: expandtab:tabstop=4:shiftwidth=4

import subprocess
import sys
import os
import json
import re

class AnsibleUtil(object):
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)))
        self.multi_ec2_path = os.path.realpath(os.path.join(self.file_path, '..','inventory','multi_ec2.py'))

    def get_inventory(self):
        cmd = [self.multi_ec2_path]
        env = {}
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE,
                         stdout=subprocess.PIPE, env=env)

        out,err = p.communicate()

        if p.returncode != 0:
            raise RuntimeError(err)

        with open('/tmp/ans.out','w') as fd:
            fd.writelines(out)
        return json.loads(out.strip())

    def get_environments(self):
        pattern = re.compile(r'^tag_environment_(.*)')

        envs = []
        inv = self.get_inventory()
        for key in inv.keys():
            m = pattern.match(key)
            if m:
                envs.append(m.group(1))

        return envs

    def get_security_groups(self):
        pattern = re.compile(r'^security_group_(.*)')

        groups = []
        inv = self.get_inventory()
        for key in inv.keys():
            m = pattern.match(key)
            if m:
                groups.append(m.group(1))

        return groups

    def get_host_address(self):
        pattern = re.compile(r'^tag_Name_(.*)')
        inv = self.get_inventory()

        inst_names = {}
        for key in inv.keys():
            m = pattern.match(key)
            if m: inst_names[m.group(1)] = inv[key]


        return inst_names




