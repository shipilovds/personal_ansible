#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Denis Shipilov <shipilovds@gmail.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

# Make coding more python3-ish, this is required for contributions to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: gnome_extension

short_description: Gnome shell extensions management

version_added: "0.99.0"

description: This module can install or enable/disable gnome shell extensions

options:
    name:
        description: This is the extension name (full name)
        required: true
        type: str
    src:
        description: Module file path or URL (to zip file)
        required: false
        type:
    force:
        description: Force module installation
        required: false
        type: bool
        default: false

    enabled:
        description: Enable module when true / disable when false
        required: false
        type: bool
        default: true

    fail_on_absent:
        description: Fail if module is absent when enabling/disabling
        required: false
        type: bool
        default: false


author:
    - Denis Shipilov (@shipilovds)
'''

EXAMPLES = r'''
- name: Install extensions
  gnome_extension:
    name: 'arcmenu@arcmenu.com'
    src: 'https://extensions.gnome.org/extension-data/arcmenuarcmenu.com.v6.shell-extension.zip'

- name: Enable/disable extensions
  gnome_extension:
    name: 'user-theme@gnome-shell-extensions.gcampax.github.com'
    enabled: True
'''

from ansible.module_utils.basic import AnsibleModule
import yaml

# Options are taken from 'DOCUMENTATION' block as the primary source of truth
ARGS_SPEC = yaml.safe_load(DOCUMENTATION)['options']

EXCLUSIVE = [('src', 'enabled'), ('name', 'force')]


def get_command(params):
    command_list = ['/usr/bin/gnome-extensions']
    if params.get('src'):
        command_list.append('install')
        if params.get('force'):
            command_list.append('--force')
        command_list.append(params['src'])
    if params.get('name') and not params.get('src'):
        if params.get('enabled'):
            command_list.append('enable')
        else:
            command_list.append('disable')
        command_list.append(params['name'])

    return command_list


def run():
    module = AnsibleModule(argument_spec=ARGS_SPEC, mutually_exclusive=EXCLUSIVE)

    result = dict(
        changed=False
    )

    name = module.params.get('name')
    src = module.params.get('src')
    force = module.params.get('force')
    fail_on_absent = module.params.get('fail_on_absent')

    if name and src and not force:
        _, ext_list, _ = module.run_command(['/usr/bin/gnome-extensions', 'list'])

    if name and src and not force and name in str(ext_list):
        module.exit_json(**result)

    rc, stdout, stderr = module.run_command(get_command(module.params))
    if stdout or stderr:
        result['stdout'] = stdout
        result['stderr'] = stderr

    if rc == 0:
        result['changed'] = True

    if src:
        acceptable_stderr = 'exists and --force was not specified'
        if rc != 0 and acceptable_stderr not in str(stderr):
            result['rc'] = rc
            module.fail_json(msg=stderr, **result)
    if name and not src:
        unacceptable_stderr = 'does not exist'
        if rc != 0 and fail_on_absent and unacceptable_stderr in str(stderr):
            result['rc'] = rc
            module.fail_json(msg=stderr, **result)

    module.exit_json(**result)


def main():
    run()


if __name__ == '__main__':
    main()
