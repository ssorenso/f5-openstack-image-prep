F5 OpenStack VE Image Preparation
=================================

|Build Status| |Docs Build Status|

- Used to patch and upload F5 VE images into OpenStack Glance.
- Accepts a single VE file and uploads it alone

Installation
------------
Git clone the repo directly to use this utility

Setup
-----
Refer to the requirements.txt file in the top-level directory to determine what needs to be installed.

VE Image Patching
-----------------
A VE image must be 'patched' to run in OpenStack. This allows for proper bootup of that instance with the correct intefaces and selfIPs.
