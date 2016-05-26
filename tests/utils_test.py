# -*- coding: utf-8 -*-

import ansible_toolkit.utils
import ConfigParser
import errno
import mock
import pytest
import unittest

from ansible_toolkit.utils import show_diff


class ColorTestCase(unittest.TestCase):

    """
    Test case for the
    ansible_toolkit.utils.(green|red|yellow|cyan|intense) functions.
    """

    def _test_output(self, color):
        self.assertTrue(self.mock_stdout.write.called)
        self.mock_stdout.write.assert_called_once_with(
            '%s%s%s\n' % (color, self.text, ansible_toolkit.utils.ENDC)
        )

    def setUp(self):
        """Setup mock object for ansible_toolkit.utils.sys.stdout."""
        self.patch_stdout = mock.patch(
            'ansible_toolkit.utils.sys.stdout', autospec=True)
        self.mock_stdout = self.patch_stdout.start()
        self.text = 'test text'

    def tearDown(self):
        """Tear down mock object for ansible_toolkit.utils.sys.stdout."""
        self.patch_stdout.stop()

    def test_cyan(self):
        """Test ansible_toolkit.utils.cyan() function."""
        self.assertIsNone(ansible_toolkit.utils.cyan(self.text))
        self._test_output(ansible_toolkit.utils.CYAN)

    def test_green(self):
        """Test ansible_toolkit.utils.green() function."""
        self.assertIsNone(ansible_toolkit.utils.green(self.text))
        self._test_output(ansible_toolkit.utils.GREEN)

    def test_intense(self):
        """Test ansible_toolkit.utils.intense() function."""
        self.assertIsNone(ansible_toolkit.utils.intense(self.text))
        self._test_output(ansible_toolkit.utils.INTENSE)

    def test_red(self):
        """Test ansible_toolkit.utils.red() function."""
        self.assertIsNone(ansible_toolkit.utils.red(self.text))
        self._test_output(ansible_toolkit.utils.RED)

    def test_yellow(self):
        """Test ansible_toolkit.utils.yellow() function."""
        self.assertIsNone(ansible_toolkit.utils.yellow(self.text))
        self._test_output(ansible_toolkit.utils.YELLOW)


class GetVaultPasswordFileTestCase(unittest.TestCase):

    """
    Test case for the
    ansible_toolkit.utils.get_vault_password_file() function.
    """

    @mock.patch('ansible_toolkit.config', autospec=True)
    def test_get(self, mock_config):
        mock_config.get.return_value = 'test'

        self.assertEqual(
            'test', ansible_toolkit.utils.get_vault_password_file())

        self.assertTrue(mock_config.get.called)
        mock_config.get.assert_called_once_with(
            'vault', 'password_file'
        )

    @mock.patch('ansible_toolkit.config', autospec=True)
    def test_nosectionerror(self, mock_config):
        mock_config.get.side_effect = ConfigParser.NoSectionError('vault')

        self.assertIsNone(ansible_toolkit.utils.get_vault_password_file())

        self.assertTrue(mock_config.get.called)
        mock_config.get.assert_called_once_with(
            'vault', 'password_file'
        )


class MkdirTestCase(unittest.TestCase):

    """Test case for the ansible_toolkit.utils.mkdir_p() function."""

    @mock.patch('ansible_toolkit.utils.os', autospec=True)
    def test_exception_catch(self, mock_os):
        mock_os.makedirs.return_value = None

        self.assertIsNone(ansible_toolkit.utils.mkdir_p('/tmp/test'))

        self.assertTrue(mock_os.makedirs.called)
        mock_os.makedirs.assert_called_once_with('/tmp/test')

    @mock.patch('ansible_toolkit.utils.os', autospec=True)
    @mock.patch('ansible_toolkit.utils.os.path', autospec=True)
    def test_exception_catch(self, mock_os_path, mock_os):
        e = OSError()
        e.errno = errno.EEXIST
        mock_os.makedirs.side_effect = e

        mock_os_path.exists.return_value = True

        self.assertIsNone(ansible_toolkit.utils.mkdir_p('/tmp/test'))

        self.assertTrue(mock_os.makedirs.called)
        mock_os.makedirs.assert_called_once_with('/tmp/test')

    @mock.patch('ansible_toolkit.utils.os', autospec=True)
    @mock.patch('ansible_toolkit.utils.os.path', autospec=True)
    def test_exception_raise(self, mock_os_path, mock_os):
        e = OSError()
        e.errno = errno.EEXIST + 1
        mock_os.makedirs.side_effect = e

        mock_os_path.exists.return_value = False

        with pytest.raises(OSError):
            self.assertIsNone(ansible_toolkit.utils.mkdir_p('/tmp/test'))

        self.assertTrue(mock_os.makedirs.called)
        mock_os.makedirs.assert_called_once_with('/tmp/test')


class ShowDiffTestCase(unittest.TestCase):

    """Test case for the ansible_toolkit.utils.show_diff() function."""

    @mock.patch('ansible_toolkit.utils.sys.stdout.write', autospec=True)
    def test_no_diff(self, mock_write):

        old = {}
        new = {}

        self.assertIsNone(show_diff(old, new))
        self.assertFalse(mock_write.called)


class SplitPathTestCase(unittest.TestCase):

    """Test case for the ansible_toolkit.utils.split_path() function."""

    def test(self):
        self.assertEqual(
            ['/', 'tmp', 'test'],
            ansible_toolkit.utils.split_path('/tmp/test'))
