#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Google
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# ----------------------------------------------------------------------------
#
#     ***     AUTO GENERATED CODE    ***    AUTO GENERATED CODE     ***
#
# ----------------------------------------------------------------------------
#
#     This file is automatically generated by Magic Modules and manual
#     changes will be clobbered when the file is regenerated.
#
#     Please read more about how to change this file at
#     https://www.github.com/GoogleCloudPlatform/magic-modules
#
# ----------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function
__metaclass__ = type

################################################################################
# Documentation
################################################################################

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ["preview"],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: gcp_pubsub_subscription_facts
description:
- Gather facts for GCP Subscription
short_description: Gather facts for GCP Subscription
version_added: 2.8
author: Google Inc. (@googlecloudplatform)
requirements:
- python >= 2.6
- requests >= 2.18.4
- google-auth >= 1.3.0
options: {}
extends_documentation_fragment: gcp
'''

EXAMPLES = '''
- name:  a subscription facts
  gcp_pubsub_subscription_facts:
      project: test_project
      auth_kind: serviceaccount
      service_account_file: "/tmp/auth.pem"
'''

RETURN = '''
items:
  description: List of items
  returned: always
  type: complex
  contains:
    name:
      description:
      - Name of the subscription.
      returned: success
      type: str
    topic:
      description:
      - A reference to a Topic resource.
      returned: success
      type: str
    pushConfig:
      description:
      - If push delivery is used with this subscription, this field is used to configure
        it. An empty pushConfig signifies that the subscriber will pull and ack messages
        using API methods.
      returned: success
      type: complex
      contains:
        pushEndpoint:
          description:
          - A URL locating the endpoint to which messages should be pushed.
          - For example, a Webhook endpoint might use "U(https://example.com/push".)
          returned: success
          type: str
    ackDeadlineSeconds:
      description:
      - This value is the maximum time after a subscriber receives a message before
        the subscriber should acknowledge the message. After message delivery but
        before the ack deadline expires and before the message is acknowledged, it
        is an outstanding message and will not be delivered again during that time
        (on a best-effort basis).
      - For pull subscriptions, this value is used as the initial value for the ack
        deadline. To override this value for a given message, call subscriptions.modifyAckDeadline
        with the corresponding ackId if using pull. The minimum custom deadline you
        can specify is 10 seconds. The maximum custom deadline you can specify is
        600 seconds (10 minutes).
      - If this parameter is 0, a default value of 10 seconds is used.
      - For push delivery, this value is also used to set the request timeout for
        the call to the push endpoint.
      - If the subscriber never acknowledges the message, the Pub/Sub system will
        eventually redeliver the message.
      returned: success
      type: int
'''

################################################################################
# Imports
################################################################################
from ansible.module_utils.gcp_utils import navigate_hash, GcpSession, GcpModule, GcpRequest
import json

################################################################################
# Main
################################################################################


def main():
    module = GcpModule(
        argument_spec=dict(
        )
    )

    if not module.params['scopes']:
        module.params['scopes'] = ['https://www.googleapis.com/auth/pubsub']

    items = fetch_list(module, collection(module))
    if items.get('subscriptions'):
        items = items.get('subscriptions')
    else:
        items = []
    return_value = {
        'items': items
    }
    module.exit_json(**return_value)


def collection(module):
    return "https://pubsub.googleapis.com/v1/projects/{project}/subscriptions".format(**module.params)


def fetch_list(module, link):
    auth = GcpSession(module, 'pubsub')
    response = auth.get(link)
    return return_if_object(module, response)


def return_if_object(module, response):
    # If not found, return nothing.
    if response.status_code == 404:
        return None

    # If no content, return nothing.
    if response.status_code == 204:
        return None

    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError) as inst:
        module.fail_json(msg="Invalid JSON response with error: %s" % inst)

    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))

    return result


if __name__ == "__main__":
    main()
