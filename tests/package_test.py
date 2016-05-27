# -*- coding: utf-8 -*-

import ansible_toolkit
import mock
import unittest


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
