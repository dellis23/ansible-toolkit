# -*- coding: utf-8 -*-

import ansible_toolkit
import mock
import unittest

from ansible_toolkit.vault import ATK_VAULT


class CloseVaultTestCase(unittest.TestCase):

    """Test case for the ansible_toolkit.close_vault() function."""

    @mock.patch('ansible_toolkit.get_vault', autospec=True)
    @mock.patch('ansible_toolkit.get_files', autospec=True)
    @mock.patch('ansible_toolkit.restore', autospec=True)
    def test(self, mock_restore, mock_get_files, mock_get_vault):
        original_file = 'tmp/test'
        encrypted_file = 'encrypted'
        vault_password_file = '/home/user/vault'

        mock_get_vault.return_value = None
        mock_get_files.return_value = [
            '%s/%s/%s' % (ATK_VAULT, original_file, encrypted_file)]

        mock_restore.return_value = None

        self.assertIsNone(ansible_toolkit.close_vault(vault_password_file))
        mock_get_vault.assert_called_once_with(vault_password_file)
        mock_get_files.assert_called_once_with(ATK_VAULT)
        mock_restore.assert_called_once_with(
            '%s' % original_file, mock_get_vault.return_value)


class OpenVaultTestCase(unittest.TestCase):

    """Test case for the ansible_toolkit.open_vault() function."""

    @mock.patch('ansible_toolkit.get_vault', autospec=True)
    @mock.patch('ansible_toolkit.get_files', autospec=True)
    @mock.patch('ansible_toolkit.backup', autospec=True)
    def test(self, mock_backup, mock_get_files, mock_get_vault):
        encrypted_file = '/tmp/test'
        vault_password_file = '/home/user/vault'

        mock_get_vault.return_value = None
        mock_get_files.return_value = [encrypted_file]

        mock_backup.return_value = None

        self.assertIsNone(ansible_toolkit.open_vault(vault_password_file))
        mock_get_vault.assert_called_once_with(vault_password_file)
        mock_get_files.assert_called_once_with('.')
        mock_backup.assert_called_once_with(
            encrypted_file, None)
