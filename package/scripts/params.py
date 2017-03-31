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

from resource_management import *
import os

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()

java64_home = config['hostLevelParams']['java_home']

hostname = config['hostname']

kibana_user = config['configurations']['kibana-env']['kibana_user']
kibana_group = config['configurations']['kibana-env']['kibana_group']

kibana_base_dir = config['configurations']['kibana-env']['kibana_base_dir']
kibana_log_dir = config['configurations']['kibana-env']['kibana_log_dir']
kibana_install_log = kibana_base_dir + '/kibana-install.log'
kibana_download = 'https://artifacts.elastic.co/downloads/kibana/kibana-5.2.2-linux-x86_64.tar.gz'
xpack_download = 'https://artifacts.elastic.co/downloads/packs/x-pack/x-pack-5.2.2.zip'

kibana_yml_template = config['configurations']['kibana-config']['kibana_yml_template']
kibana_pid_dir = config['configurations']['kibana-env']['kibana_pid_dir']
kibana_pid_file = format("{kibana_pid_dir}/kibana.pid")
xpack_security_ssl_certs_template = config['configurations']['kibana-config']['xpack_security_ssl_certs_template']
kibana_install_tmp_dir = kibana_base_dir + '/tmp'
copy_es_certs = str(config['configurations']['kibana-config']['copy_es_certs']).lower()
es_certs_file = config['configurations']['kibana-config']['es_certs_file']
