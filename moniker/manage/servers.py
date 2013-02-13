# Copyright 2012 Managed I.T.
#
# Author: Kiall Mac Innes <kiall@managedit.ie>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from moniker.openstack.common import log as logging
from moniker.manage import base
from moniker.central import api as central_api

LOG = logging.getLogger(__name__)


class ListServersCommand(base.ListCommand):
    """ List Servers """

    def execute(self, parsed_args):
        return central_api.get_servers(self.context)


class GetServerCommand(base.GetCommand):
    """ Get Server """

    def get_parser(self, prog_name):
        parser = super(GetServerCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Server ID")

        return parser

    def execute(self, parsed_args):
        return central_api.get_server(self.context, parsed_args.id)


class CreateServerCommand(base.CreateCommand):
    """ Create Server """

    def get_parser(self, prog_name):
        parser = super(CreateServerCommand, self).get_parser(prog_name)

        parser.add_argument('--name', help="Server Name", required=True)
        parser.add_argument('--ipv4', help="Server IPv4 Address")
        parser.add_argument('--ipv6', help="Server IPv6 Address")

        return parser

    def execute(self, parsed_args):
        server = dict(
            name=parsed_args.name,
            ipv4=parsed_args.ipv4,
            ipv6=parsed_args.ipv6,
        )

        return central_api.create_server(self.context, server)


class UpdateServerCommand(base.UpdateCommand):
    """ Update Server """

    def get_parser(self, prog_name):
        parser = super(UpdateServerCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Server ID")
        parser.add_argument('--name', help="Server Name")

        ipv4_group = parser.add_mutually_exclusive_group()
        ipv4_group.add_argument('--ipv4', help="Server IPv4 Address")
        ipv4_group.add_argument('--no-ipv4', action='store_true')

        ipv6_group = parser.add_mutually_exclusive_group()
        ipv6_group.add_argument('--ipv6', help="Server IPv6 Address")
        ipv6_group.add_argument('--no-ipv6', action='store_true')

        return parser

    def execute(self, parsed_args):
        server = {}

        if parsed_args.name:
            server['name'] = parsed_args.name

        if parsed_args.no_ipv4:
            server['ipv4'] = None
        elif parsed_args.ipv4:
            server['ipv4'] = parsed_args.ipv4

        if parsed_args.no_ipv6:
            server['ipv6'] = None
        elif parsed_args.ipv6:
            server['ipv6'] = parsed_args.ipv6

        return central_api.update_server(self.context, parsed_args.id, server)


class DeleteServerCommand(base.DeleteCommand):
    """ Delete Server """

    def get_parser(self, prog_name):
        parser = super(DeleteServerCommand, self).get_parser(prog_name)

        parser.add_argument('id', help="Server ID")

        return parser

    def execute(self, parsed_args):
        return central_api.delete_server(self.context, parsed_args.id)
