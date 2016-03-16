# Copyright 2015-2016 F5 Networks Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""OpenStack base library class"""
import os


class OpenStackCreds(object):
    """OpenStack Credentials"""
    def __init__(self, auth_url, tenant_name, username, password):
        self.auth_url = auth_url
        self.tenant_name = tenant_name
        self.username = username
        self.password = password


class OpenStackLib(object):
    """OpenStack Library"""
    def __init__(self, creds, extensions=None):
        if creds is None:
            raise ValueError('Creds must be supplied')

        self.creds = creds
        self.extensions = extensions

    def print_creds(self):
        """Print creds for debug purposes"""
        creds_str = 'OpenStackLib:Creds [%s/%s/%s]' % (
            self.creds.tenant_name, self.creds.username,
            self.creds.password)
        self.print_context.heading('%s', creds_str)


def get_creds():
    """Get creds based on arg input."""
    os_tenant_name = None
    os_username = None
    os_password = None
    os_auth_url = None

    # Start with environment variables
    try:
        os_tenant_name = os.environ['OS_TENANT_NAME']
    except KeyError:
        pass

    try:
        os_username = os.environ['OS_USERNAME']
    except KeyError:
        pass

    try:
        os_password = os.environ['OS_PASSWORD']
    except KeyError:
        pass

    try:
        os_auth_url = os.environ['OS_AUTH_URL']
    except KeyError:
        pass

    creds = OpenStackCreds(
        os_auth_url,
        os_tenant_name,
        os_username,
        os_password)
    return creds
