# -*- coding: utf-8 -*-

import ansible


class AnsibleDao(object):

    """Interface for Ansible Data Access Object implementation."""

    __slots__ = ('version',)

    def __init__(self):
        self.version = ansible.__version__

    def get_vault(self, vault_password_file):
        """
        Returns the Ansible vault.

        :param vault_password_file:
            the path to the Ansible vault password file.
        :return: VaultLib
        """
        raise NotImplementedError

    def get_vault_password(self, vault_password_file=None):
        """
        Returns the vault password.

        Read a vault password from a file.

        :param vault_password_file:
            the path to the Ansible vault password file.
        :return: the vault password.
        """
        raise NotImplementedError

    def show_variables(
            self, host, inventory_file=None, vault_password_file=None):
        """

        :param host: the host name for which you want to display variables.
        :param inventory_file: the inventory.
        :param vault_password_file:
            the path to the Ansible vault password file.
        """
        raise NotImplementedError


def create_dao():
    """
    Creates an Ansible data access object implementation that
    implements the dao.AnsibleDao interface.

    :return: Ansible data access object.
    """
    if ansible.__version__.startswith('2.0') or \
            ansible.__version__.startswith('2.1'):
        from ansible_toolkit.ansible20 import AnsibleDaoImpl
        return AnsibleDaoImpl()
    elif ansible.__version__.startswith('1.9'):
        from ansible_toolkit.ansible19 import AnsibleDaoImpl
        return AnsibleDaoImpl()
    else:
        raise NotImplementedError(
            'There is no DAO implementation for Ansible version %s' %
            ansible.__version__)
