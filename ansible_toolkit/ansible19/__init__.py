# -*- coding: utf-8 -*-

import ansible
import ansible_toolkit
import ansible_toolkit.utils
import ConfigParser
import os.path

from ansible_toolkit.dao import AnsibleDao

from ansible.runner import Runner
from ansible.inventory import Inventory
from ansible.utils.vault import VaultLib
from ansible.utils import combine_vars, read_vault_file, template


class AnsibleDaoImpl(AnsibleDao):

    """Ansible 1.9.x  implementation."""

    __slots__ = ('vault_password_file', 'version')

    def __init__(self):
        super(AnsibleDaoImpl, self).__init__()

        if not self.version.startswith('1.9'):
            raise NotImplementedError(
                'Cannot use Ansible 1.9.x implementation with Ansible %s!' %
                ansible.__version__)

    def get_inventory(self, inventory_path=None, vault_password_path=None):
        if inventory_path is None:
            try:
                inventory_path = os.path.expanduser(
                    ansible_toolkit.config.get('inventory', 'path'))
            except ConfigParser.NoSectionError:
                inventory_path = 'inventory'
        vault_password = self.get_vault(vault_password_path)
        return Inventory(inventory_path, vault_password=vault_password)

    def get_vault(self, vault_password_file=None):
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
            return read_vault_file(
                ansible_toolkit.utils.get_vault_password_file())
        return read_vault_file(vault_password_file)

    def show_variables(
            self, host, inventory_path=None, vault_password_file=None):
        """

        :param host:
            the host name for which you want to display variables.
        :param inventory_path: the path to the Ansible inventory.
        :param vault_password_file:
            the path to the Ansible vault password file.
        """
        inventory = self.get_inventory(inventory_path, vault_password_file)
        Runner.get_inject_vars = get_inject_vars
        runner = Runner(inventory=inventory)
        return runner.get_inject_vars(host)


def get_inject_vars(self, host):

    host_variables = self.inventory.get_variables(
        host, vault_password=self.vault_pass)
    ansible_host = self.inventory.get_host(host)

    # Keep track of variables in the order they will be merged
    to_merge = [
        ('Default Variables', self.default_vars),
    ]

    # Group variables
    groups = ansible_host.get_groups()
    for group in sorted(groups, key=lambda g: g.depth):
        to_merge.append(
            ("Group Variables ({})".format(group.name), group.get_variables())
        )

    combined_cache = self.get_combined_cache()

    # use combined_cache and host_variables to template the module_vars
    # we update the inject variables with the data we're about to template
    # since some of the variables we'll be replacing may be contained there too
    module_vars_inject = combine_vars(
        host_variables, combined_cache.get(host, {}))
    module_vars_inject = combine_vars(
        self.module_vars, module_vars_inject)
    module_vars = template.template(
        self.basedir, self.module_vars, module_vars_inject)

    to_merge.extend([
        ('Host Variables', ansible_host.vars),
        ('Setup Cache', self.setup_cache.get(host, {})),
        ('Play Variables', self.play_vars),
        ('Play File Variables', self.play_file_vars),
        ('Role Variables', self.role_vars),
        ('Module Variables', module_vars),
        ('Variables Cache', self.vars_cache.get(host, {})),
        ('Role Parameters', self.role_params),
        ('Extra Variables', self.extra_vars),
    ])
    all_vars = {}
    for name, value in to_merge:
        old_inject = all_vars
        all_vars = combine_vars(all_vars, value)
        all_vars[name] = (old_inject, all_vars)

    return all_vars
