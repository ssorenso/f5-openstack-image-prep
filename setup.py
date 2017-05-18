# Copyright 2014 F5 Networks Inc.
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

from setuptools import setup

import f5_image_prep

setup(
    name='f5_image_prep',
    description='Tooling for creating Openstack Ready VEs',
    license='Apache License, Version 2.0',
    version=f5_image_prep.__version__,
    author='F5 Networks',
    author_email='f5_image_prep@f5.com',
    url='https://github.com/F5Networks/f5-openstack-image-prep',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: System Administrators',
    ],
    install_requires=['python-keystoneclient == 1.7.2',
                      'python-glanceclient == 1.2.0']
)
