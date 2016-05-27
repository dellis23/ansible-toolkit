# -*- coding: utf-8 -*-

import ConfigParser
import ansible_toolkit.dao
import os
import os.path

from .dao import create_dao
from .utils import get_files, split_path
from .vault import ATK_VAULT, backup, restore


config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.atk')])


def close_vault(vault_password_file=None):
    """
    :param vault_password_file:
        the path to the Ansible vault password file.
    """
    ansible_vault = get_vault(vault_password_file)

    for file_ in get_files(ATK_VAULT):
        if os.path.basename(file_) == 'encrypted':

            # Get the path without the atk vault base and encrypted filename
            original_path = os.path.join(*split_path(file_)[1:-1])
            restore(original_path, ansible_vault)


def gather_facts(host, inventory=None, user=None):
    """
    :param host:
    :param inventory:
    :param user:
    :return:
    """
    return ansible_toolkit.dao.create_dao().gather_facts(host, inventory, user)


def get_vault(vault_password_file):
    """
    Returns the Ansible vault.

    :param vault_password_file:
        the path to the Ansible vault password file.
    :return: VaultLib
    """
    return create_dao().get_vault(vault_password_file)


def open_vault(vault_password_file=None):
    """
    :param vault_password_file:
        the path to the Ansible vault password file.
    """
    ansible_vault = get_vault(vault_password_file)

    for file_ in get_files('.'):
        backup(file_, ansible_vault)


def show_variables(host, inventory_path=None, vault_password_file=None):
    """

    :param host: the host name for which you want to display variables.
    :param inventory_path: the path to the Ansible inventory.
    :param vault_password_file:
        the path to the Ansible vault password file.
    """
    return create_dao().show_variables(
        host, inventory_path, vault_password_file)


def show_template(host, path, gather_facts=True,
                  inventory_file=None, password_file=None,
                  user=None):
    dao_instance = create_dao()
    inventory = dao_instance.get_inventory(
        inventory_file, password_file)
    setup_cache = dao_instance.gather_facts(
        host, inventory, user) if gather_facts else {}

    host_vars = dao_instance.get_host_variables(
        host, inventory, setup_cache)

    return dao_instance.template_from_file('.', path, host_vars)
