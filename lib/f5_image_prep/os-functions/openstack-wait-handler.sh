#!/bin/bash

# Copyright 2017 F5 Networks Inc.
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

source /config/os-functions/openstack-datasource.sh

# OpenStack wait condition notification settings

function wait_condition_notify() {

    local wc_notify=$(get_user_data_value {bigip}{wait_condition_notify})

    if [[ $(is_false ${wc_notify}) ]]; then
	    log "Wait Condition will not be notified..."
	else
	    log "Notifying Wait Condition"
        eval ${wc_notify}
	fi
}
