#!/usr/bin/env python

"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys
import os
import glob
import pwd
import grp
import signal
import time
from resource_management import *
from kibana_common import kill_process


class Master(Script):
    def install(self, env):
        import params

        env.set_params(params)
        self.install_packages(env)

        try:
            grp.getgrnam(params.kibana_group)
        except KeyError:
            Group(group_name=params.kibana_group)

        try:
            pwd.getpwnam(params.kibana_user)
        except KeyError:
            User(username=params.kibana_user,
                 gid=params.kibana_group,
                 groups=[params.kibana_group],
                 ignore_failures=True
                 )

        Directory(
            [params.kibana_base_dir, params.kibana_pid_dir, params.kibana_log_dir, params.kibana_install_tmp_dir],
            mode=0755,
            cd_access='a',
            owner=params.kibana_user,
            group=params.kibana_group,
            create_parents=True
        )

        File(params.kibana_install_log,
             mode=0644,
             owner=params.kibana_user,
             group=params.kibana_group,
             content=''
             )

        cmd = format("cd {kibana_base_dir}; wget {kibana_download} -O kibana.tar.gz -a {kibana_install_log}")
        Execute(cmd, user=params.kibana_user)

        cmd = format("cd {kibana_base_dir}; tar -xf kibana.tar.gz --strip-components=1")
        Execute(cmd, user=params.kibana_user)

        # Download x-pack
        cmd = format("cd {kibana_base_dir}; wget {xpack_download} -O x-pack.zip -a {kibana_install_log}")
        Execute(cmd, user=params.kibana_user)

        cmd = format("cd {kibana_base_dir}; bin/kibana-plugin install file://{kibana_base_dir}/x-pack.zip")
        Execute(cmd)

        if params.copy_es_certs == 'true':
            cmd = format("unzip {es_certs_file} -d {kibana_base_dir}/. ")
            Execute(cmd)

        cmd = format("chown -R {kibana_user}:{kibana_group} {kibana_base_dir}")
        Execute(cmd)

        cmd = format("cd {kibana_base_dir}; rm kibana.tar.gz")
        Execute(cmd, user=params.kibana_user)

        Execute('echo "Install complete"')

    def configure(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # This allows us to access the params.elastic_pid_file property as
        # format('{elastic_pid_file}')
        env.set_params(params)

        configurations = params.config['configurations']['kibana-config']
        kibana_yml_template_content = InlineTemplate(configurations['kibana_yml_template'],
                                                     configurations=configurations)

        File(format("{kibana_base_dir}/config/kibana.yml"),
             content=kibana_yml_template_content,
             owner=params.kibana_user,
             group=params.kibana_user
             )

        # Ensure all files owned by elasticsearch user
        cmd = format("chown -R {kibana_user}:{kibana_group} {kibana_base_dir}")
        Execute(cmd)

        Execute('echo "Configuration complete"')

    def stop(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        env.set_params(params)

        # Stop kibana
        kill_process(params.kibana_pid_file, params.kibana_user, params.kibana_log_dir)

    def start(self, env):
        # Import properties defined in -config.xml file from the params class
        import params

        # This allows us to access the params.elastic_pid_file property as
        #  format('{elastic_pid_file}')
        env.set_params(params)

        # Configure Elasticsearch
        self.configure(env)

        # Start Elasticsearch
        cmd = format("{kibana_base_dir}/bin/kibana >> {kibana_log_dir}/kibana.log &")
        Execute(cmd, user=params.kibana_user)

    def status(self, env):
        # Import properties defined in -env.xml file from the status_params class
        import status_params

        # This allows us to access the params.elastic_pid_file property as
        #  format('{elastic_pid_file}')
        env.set_params(status_params)

        # try:
        #    pid_file = glob.glob(status_params.elastic_pid_file)[0]
        # except IndexError:
        #    pid_file = ''

        # Use built-in method to check status using pidfile
        check_process_status(status_params.kibana_pid_file)


if __name__ == "__main__":
    Master().execute()
