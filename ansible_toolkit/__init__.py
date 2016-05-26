# -*- coding: utf-8 -*-

import ConfigParser
import os.path

from .dao import create_dao

config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.atk')])


def get_vault(vault_password_file):
    """
    Returns the Ansible vault.

    :param vault_password_file:
        the path to the Ansible vault password file.
    :return: VaultLib
    """
    dao = create_dao()
    return dao.get_vault(vault_password_file)


def show_variables(host, inventory_path=None, vault_password_file=None):
    """

    :param host: the host name for which you want to display variables.
    :param inventory_path: the path to the Ansible inventory.
    :param vault_password_file:
        the path to the Ansible vault password file.
    """
    dao = create_dao()
    return dao.show_variables(
        host, inventory_path, vault_password_file)
