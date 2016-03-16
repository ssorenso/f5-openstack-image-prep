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

"""OpenStack Build-Up Functionality."""
from f5_image_prep.openstack.client import get_keystone_client
from f5_image_prep.openstack.openstack import OpenStackLib

TENANT_MEMBER_ROLE = '_member_'


class KeystoneLib(OpenStackLib):
    """Keystone library operations"""
    def __init__(self, creds):
        if creds and creds.tenant_name != 'admin':
            raise ValueError(
                'Tenant %s is incorrect. Must be admin' % creds.tenant_name)
        OpenStackLib.__init__(self, creds)
        self.keystone_client = get_keystone_client(creds)

    def get_all_non_admin_tenants(self):
        """Get all non-admin tenants"""
        tenants = self.keystone_client.tenants.list()
        return_tenants = []
        for tenant in tenants:
            if tenant.name == 'admin' or tenant.name == 'service':
                continue
            return_tenants.append(tenant)
        return return_tenants

    def get_tenant(self, name):
        """Get tenant by name"""
        tenants = self.keystone_client.tenants.list()
        for tenant in tenants:
            if tenant.name == name:
                return tenant
        return None

    def get_tenant_by_id(self, tenant_id):
        """Get tenant by id"""
        tenants = self.keystone_client.tenants.list()
        for tenant in tenants:
            if tenant.id == tenant_id:
                return tenant
        return None

    def create_tenant(self, name, description):
        """Create a tenant"""
        self.print_context.heading('Create tenant %s.', name)
        tenant = self.get_tenant(name)
        if tenant:
            self.print_context.debug('Tenant %s already exists.', name)
            return tenant

        tenant = self.keystone_client.tenants.create(
            name, description=description, enabled=True)

        self.obj_check.openstack('tenant created', True, self.get_tenant, name)

        self.print_context.debug('Created tenant %s.', name)
        return tenant

    def delete_tenant(self, name):
        """Delete a tenant"""
        self.print_context.heading('Delete tenant %s.', name)
        if name == 'admin':
            raise Exception('Tenant %s should not be deleted.' % name)

        tenant = self.get_tenant(name)
        if not tenant:
            self.print_context.debug(
                'Tenant does not exist.  Skipping tenant-based cleanup.')
            return

        self.keystone_client.tenants.delete(tenant)

        self.obj_check.openstack(
            'tenant deleted', False, self.get_tenant, name)

        self.print_context.debug('Deleted tenant %s.', name)

    def get_user(self, name):
        """Get user by name"""
        user_list = self.keystone_client.users.list()
        for user in user_list:
            if user.name == name:
                return user
        return None

    def create_user(self, tenant, name, password, email):
        """Create a user"""
        self.print_context.heading(
            'Create tenant %s user %s.', tenant.name, name)
        user = self.get_user(name)
        if user:
            self.print_context.debug('User %s already exists.', name)
            return user

        user = self.keystone_client.users.create(
            name=name, password=password, tenant_id=tenant.id, email=email)

        self.obj_check.openstack('user created', True, self.get_user, name)

        self.print_context.debug(
            'Created tenant %s user %s.', tenant.name, name)
        return user

    def delete_user(self, name):
        """Delete a user"""
        self.print_context.heading('Delete user %s.', name)
        if name == 'admin':
            raise Exception('User %s should not be deleted.' % name)

        user = self.get_user(name)
        if not user:
            self.print_context.debug('User does not exist.')
            return

        tenant = self.get_tenant_by_id(user.tenantId)
        if not tenant:
            raise Exception('No tenant found for tenant id %s', user.tenantId)

        self.keystone_client.users.delete(user)

        self.obj_check.openstack('user deleted', False, self.get_user, name)

        self.print_context.debug(
            'Deleted tenant %s user %s.', tenant.name, name)

    def get_member_role(self):
        """Get member role"""
        roles = self.keystone_client.roles.list()
        for role in roles:
            if role.name == TENANT_MEMBER_ROLE:
                return role
        raise Exception('Member role was not found.')

    def __check_user_role(self, check_tenant_id, check_user_id, check_role_id):
        """Check if a user has a role"""
        roles = self.keystone_client.roles.roles_for_user(
            user=check_user_id, tenant=check_tenant_id)

        for role in roles:
            if role.id == check_role_id:
                return True
        return False

    def add_user_member_role(self, tenant, user):
        """Give a user Member role for a tenant"""
        self.print_context.heading(
            'Add user member role for tenant %s user %s.',
            tenant.name, user.name)

        member_role = self.get_member_role()
        if self.__check_user_role(tenant.id, user.id, member_role.id):
            self.print_context.debug(
                'User %s already has member role.', user.name)
            return

        self.keystone_client.roles.add_user_role(
            role=member_role, user=user.id, tenant=tenant.id)

        self.obj_check.openstack(
            'user role added', True, self.__check_user_role, tenant.id,
            user.id, member_role.id)

        self.print_context.debug(
            'Added member role to tenant %s user %s.', tenant.name, user.name)
