# -*- coding: utf-8 -*-

import ansible

from ansible.cli import CLI
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.vault import VaultLib
from ansible.vars import VariableManager

from ansible_toolkit.dao import AnsibleDao


class AnsibleDaoImpl(AnsibleDao):

    """Ansible 2.0.x implementation."""

    __slots__ = ('vault_password_file', 'version')

    def __init__(self):
        super(AnsibleDaoImpl, self).__init__()

        if not self.version.startswith('2'):
            raise NotImplementedError(
                'Cannot use Ansible 2.0.x implementation with Ansible %s!' %
                ansible.__version__)
        self.vault_password_file = None

    def get_vault(self, vault_password_file):
        """
        Returns the Ansible vault.

        :param vault_password_file:
            the path to the Ansible vault password file.
        :return: VaultLib
        """
        return VaultLib(self.get_vault_password(vault_password_file))

    def get_vault_password(self, vault_password_file=None):
        """
        Returns the vault password.

        Read a vault password from a file.

        :param vault_password_file:
            the path to the Ansible vault password file.
        :return: the vault password.
        """
        if vault_password_file is None:
            return self.read_vault_file(
                ansible_toolkit.utils.get_vault_password_file())
        return CLI.read_vault_password_file(vault_password_file, DataLoader())

    def read_vault_file(self, vault_password_file):
        """

        :param vault_password_file:
        :return:
        """
        from ansible.cli import CLI
        from ansible.parsing.dataloader import DataLoader

        return CLI.read_vault_password_file(vault_password_file, DataLoader())

    def show_variables(
            self, host, inventory_path=None, vault_password_file=None):
        """

        :param host: the host name for which you want to display variables.
        :param inventory_path: the path to the Ansible inventory.
        :param vault_password_file:
            the path to the Ansible vault password file.
        """
        variable_manager = VariableManager()
        loader = DataLoader()
        inventory = Inventory(
            loader=loader, variable_manager=variable_manager, host_list=[host])
        variable_manager.set_inventory(inventory)
