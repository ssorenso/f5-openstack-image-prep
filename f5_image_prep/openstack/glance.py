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
from f5_image_prep.openstack.client import get_glance_client
from f5_image_prep.openstack.openstack import OpenStackLib


class GlanceLib(OpenStackLib):
    """Glance library operations"""
    def __init__(self, creds):
        OpenStackLib.__init__(self, creds)
        self.glance_client = get_glance_client(creds)

    def get_image(self, name):
        """Get image by name"""
        images = self.glance_client.images.list()
        for image in images:
            if image.name == name:
                return image
        return None

    def create_image(self, name, path, disk_format, container_format):
        """Upload/Import an image"""
        self.print_context.heading('Create image %s.', name)
        image = self.get_image(name)
        if image:
            self.print_context.debug('Image %s already exists.', name)
            return image

        with open(path) as file_image:
            image = self.glance_client.images.create(
                name=name,
                is_public=True,
                disk_format=disk_format,
                container_format=container_format,
                data=file_image)

        self.obj_check.openstack('image created', True, self.get_image, name)

        self.print_context.debug('Created image %s.', name)
        return image

    def delete_image(self, name):
        """Delete image"""
        self.print_context.heading('Delete image %s.', name)

        image = self.get_image(name)
        if not image:
            self.print_context.debug('Image %s does not exist.', name)
            return image

        self.glance_client.images.delete(image.id)

        self.obj_check.openstack('image deleted', False, self.get_image, name)

        self.print_context.debug('Deleted image %s.', name)
