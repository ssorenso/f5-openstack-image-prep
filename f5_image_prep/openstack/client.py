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

import re

import glanceclient.v1.client as gclient
import keystoneclient.v2_0.client as ksclient


class AuthURLNotSet(KeyError):
    pass


def get_keystone_client(creds):
    """Create keystone client."""
    return ksclient.Client(username=creds.username,
                           password=creds.password,
                           tenant_name=creds.tenant_name,
                           auth_url=creds.auth_url)


def _strip_version(endpoint):
    """Strip version from the last component of endpoint if present."""
    if endpoint.endswith('/'):
        endpoint = endpoint[:-1]
    url_bits = endpoint.split('/')
    if re.match(r'v\d+\.?\d*', url_bits[-1]):
        endpoint = '/'.join(url_bits[:-1])
    return endpoint


def get_glance_client(creds):
    """Create glance client"""
    keystone_client = get_keystone_client(creds)
    # If you don't strip the version, the v1 client lists will
    # try to use /v2/v1/images which is wrong
    glance_endpoint = _strip_version(
        keystone_client.service_catalog.url_for(
            service_type='image',
            endpoint_type='publicURL'
        )
    )
    return gclient.Client(glance_endpoint, token=keystone_client.auth_token)
