# Personal ansible repo for my workstation
"One ring to rule them all"

## Guaranteed compatibility with OS

- Fedora 36

## Requirements

- ansible-core >= 2.12
- [shipilovds.workstation](https://github.com/shipilovds/workstation) collection

### Requirements installation

To install `ansible`:

```bash
pip install ansible
```

To install `shipilovds.workstation` collection:

```bash
ansible-galaxy collection install -r requirements.yml
```

## Additional files

I use ansible-vault password file `.vault_key` (`vault_password_file` in [ansible.cfg](https://github.com/shipilovds/personal_ansible/blob/master/ansible.cfg)) to store my secure variables inside `vars/enctypted.yml`

## About variables

`vars/general.yml` contains all necessary variables that I need to setup my workstations.

`vars/encrypted.yml` contains several encrypted variables I don't want to expose (obviously):
 - services_shadowsocks_conf
 - tools_pypirc_token
 - tools_user_name
 - tools_user_privkey
 - tools_user_privkey_filename
 - tools_user_pubkey

> See [roles documentation](https://github.com/shipilovds/workstation/blob/latest/docs/roles.md) for more details.

## Usage

```
ansible-playbook playbook.yml [-t tags(comma separated list)]
```
