f5-openstack-image-prep
=======================

|slack badge|

Introduction
------------

The standard F5® BIG-IP® Virtual Edition (VE) images available from f5.com must be 'patched' in order to be compatible with OpenStack. This repository's contents make it possible to patch and upload F5® VE images into OpenStack Glance.

The easiest way to patch a VE image for use in OpenStack is to use the F5® Heat template 'patch_upload_ve_image.yaml'. Please see the `F5® Heat User Guide <http://f5-openstack-heat.readthedocs.io/en/latest/map_heat-user-guide.html>`_ for instructions.

For Developers
--------------

VE Image Patching
~~~~~~~~~~~~~~~~~
A VE image must be 'patched' to run in OpenStack. This allows for proper bootup of the instance with the correct interfaces and selfIPs. The ``patch-image.sh`` script in ``bin/`` does this work. If you would like to patch a VE image in a specific way other than what is provided in the ``ve_image_sync.py`` tool, you can use the ``patch-image.sh`` script directly:

``sudo /bin/bash patch-image.sh -f -s <your_startup_script> BIGIP_11.6.qcow2``

The above command patches the BIGIP_11.6.qcow2 image to be firstboot and injects a user-defined startup script before producing a patched image. The patched image will be created in $HOME/.f5-image-prep/tmp if no -o (output file) is specified. A minimal execution of the script might look like the following:

``sudo /bin/bash patch-image.sh -f BIG_11.6.qcow2``

Setup
~~~~~

To install the project requirements:

``sudo pip install -R requirements.txt``


Installation
~~~~~~~~~~~~
You can either clone this repo, or use the command below to install it using ``pip``.

``sudo pip install git+https://github.com/F5Networks/f5-openstack-image-prep.git``


Updating Code
~~~~~~~~~~~~~
Note that any updates to code in lib/f5_image_prep have to be tar'ed up in startup.tar as well.

Filing Issues
-------------
See the Issues section of `Contributing <CONTRIBUTING.md>`_.

Contributing
------------
See `Contributing <CONTRIBUTING.md>`_.

Copyright
---------
Copyright 2016 F5 Networks Inc.


License
-------

Apache V2.0
~~~~~~~~~~~
Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations
under the License.

Contributor License Agreement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Individuals or business entities who contribute to this project must have
completed and submitted the `F5 Contributor License Agreement
<http://f5-openstack-docs.readthedocs.org/en/latest/cla_landing.html>`__
to Openstack_CLA@f5.com prior to their code submission being included in this
project.


.. |slack badge| image:: https://f5-openstack-slack.herokuapp.com/badge.svg
    :target: https://f5-openstack-slack.herokuapp.com/
    :alt: Slack
