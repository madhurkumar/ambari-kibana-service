# Ambari Kibana Service

The Ambari Kibana Service is a custom service for Ambari that allows you to install and manage Kibana via Ambari along with x-pack.  This service is provided as a community project and is not supported by Hortonworks.  Futhermore, this service is intended for testing and development and should not be used in a production environment.  This service is for Ambari 2.4.x and Kibana/Elasticsearch 5.2.2.

## Please note x-pack is licensed component and this service is not responsible for managing license.

## Installation

To install this service, you need access to the Ambari Server with sudo permissions.

```
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
sudo git clone https://github.com/madhurkumar/ambari-kibana-service /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/KIBANA
```

If you do not have the ability to use git, you can download the repo archive and extract it to directory shown above.

After you have installed the service, you need to restart the Ambari Server.

```
sudo service ambari-server restart
```

Once the Ambari Server service has been restarted, you should see Kibana as an available service to install from the Add Service screen.

## Compatibility

This service has been tested with the following:

- RHEL 7.x
- Ambari 2.4.2.0
- Kibana 5.2.2
- Elasticsearch 5.2.2

## Limitations

The following limitations currently apply:

- The service does not currently have Ambari Service Advisor or Ambari Alert functionality.

## License

Licensed under the Apache License, Version 2.0 (the “License”); you may not use this file except in compliance with the License.

You may obtain a copy of the License at

<http://www.apache.org/licenses/LICENSE-2.0>

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an “AS IS” BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
