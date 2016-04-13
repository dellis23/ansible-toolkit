# -*- coding: utf-8 -*-

import ansible


class AnsibleDao(object):
    """
    Interface for Ansible Data Access Object implementation.
    """

    def __init__(self):
        self.version = ansible.__version__

    def get_vault_lib(self):
        """
        Returns the Ansible VaultLib class.
        """
        raise NotImplementedError

    def read_vault_file(vault_password_file):
        """
        Read a vault password from a file or if executable,
        execute the script and
        retrieve password from STDOUT
        """
        raise NotImplementedError


class Ansible2(AnsibleDao):
    """
    Ansible 2.x implementation.
    """

    def __init__(self):
        if not ansible.__version__.startswith('2'):
            raise NotImplementedError(
                    'Cannot use Ansible 2.x implementation with Ansible 1.x!')

    def get_vault_lib(self):
        from ansible.parsing.vault import VaultLib
        return VaultLib

    def read_vault_file(self, vault_password_file):
        from ansible.cli import CLI
        from ansible.parsing.dataloader import DataLoader

        return CLI.read_vault_password_file(vault_password_file, DataLoader())


class Ansible1(AnsibleDao):
    """
    Ansible 1.x implementation.
    """

    def __init__(self):
        if not ansible.__version__.startswith('1'):
            raise NotImplementedError(
                    'Cannot use Ansible 1.x implementation with Ansible 2.x!')

    def get_vault_lib(self):
        from ansible.utils.vault import VaultLib
        return VaultLib

    def read_vault_file(self, vault_password_file):
        from ansible.utils import read_vault_file
        return read_vault_file(vault_password_file)


def create_dao():
    """
    Creates an Ansible data access object implementation that
    implements the dao.AnsibleDao interface.

    :return: Ansible data access object.
    """

    if ansible.__version__.startswith('2'):
        return Ansible2()
    return Ansible1()
