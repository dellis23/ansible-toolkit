# -*- coding: utf-8 -*-

import ansible_toolkit.vault
import hashlib
import mock
import unittest

from ansible_toolkit.vault import ATK_VAULT


class VaultTestCase(unittest.TestCase):

    """Test case for the ansible_toolkit.vault module."""

    @mock.patch('ansible_toolkit.vault.os.remove', autospec=True)
    def test_restore(self, mock_os_remove):
        """Test for the ansible_toolkit.vault.restore() function."""

        path = '/tmp/test'
        old_data = '123'
        old_hash = hashlib.sha1(old_data).hexdigest()
        new_data = '1234'
        encrypted_data = 'encrypted'

        m = mock.mock_open()
        m.side_effect = [
            mock.mock_open(read_data=old_data).return_value,
            mock.mock_open(read_data=old_hash).return_value,
            mock.mock_open(read_data=new_data).return_value,
            mock.mock_open().return_value,
        ]
        with mock.patch('ansible_toolkit.vault.open', m):
            mock_vault = mock.MagicMock()
            mock_vault.encrypt.return_value = encrypted_data

            ansible_toolkit.vault.restore(path, mock_vault)

            m.assert_called()
            m.assert_has_calls([
                mock.call('%s/encrypted' % path, 'rb'),
                mock.call('%s/hash' % path, 'rb'),
                mock.call(path, 'rb'),
                mock.call(path, 'wb')])
            mock_vault.encrypt.assert_called_once_with(new_data)
            mock_os_remove.assert_called()
            mock_os_remove.assert_has_calls([
                mock.call('%s/encrypted' % path),
                mock.call('%s/hash' % path)])
