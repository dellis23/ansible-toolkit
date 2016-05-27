# -*- coding: utf-8 -*-


import ansible
import ansible_toolkit
import mock
import pytest
import unittest

from ansible_toolkit.dao import AnsibleDao


class CreateDaoTestCase(unittest.TestCase):

    """
    Test case for the
    ansible_toolkit.dao.create_dao() function.
    """

    def test(self):
        dao = ansible_toolkit.dao.create_dao()
        self.assertIsNotNone(dao)
        self.assertEqual(ansible.__version__, dao.version)

    @mock.patch('ansible_toolkit.dao.ansible', autospec=True)
    def test_no_implementation(self, mock_ansible):
        """No implementation exists for the given Ansible version"""
        mock_ansible.__version__ = '100.0.1'

        with pytest.raises(NotImplementedError):
            ansible_toolkit.dao.create_dao()


class InitTestCase(unittest.TestCase):

    """
    Test case for the
    ansible_toolkit.dao.AnsibleDao.__init__() function.
    """

    def test(self):
        dao = AnsibleDao()
        self.assertEqual(ansible.__version__, dao.version)


class InterfaceTestCase(unittest.TestCase):

    """
    Test case to verify ansible_toolkit.dao.AnsibleDao
    interface contract that needs to be implemented by
    its implementations.
    """

    def test_interface(self):
        """Test functions to be implemented."""
        interface = AnsibleDao()

        with pytest.raises(NotImplementedError):
            interface.gather_facts(None)

        with pytest.raises(NotImplementedError):
            interface.get_vault(None)

        with pytest.raises(NotImplementedError):
            interface.get_vault_password(None)

        with pytest.raises(NotImplementedError):
            interface.template_from_file(None, None, None, None)

        with pytest.raises(NotImplementedError):
            interface.show_variables(None)


class ShowVariablesTestCase(unittest.TestCase):

    """
    Test case for the
    ansible_toolkit.dao.AnsibleDao.show_variables() function.
    """

    def setUp(self):
        self.dao = ansible_toolkit.dao.create_dao()

    def test(self):
        """
        """

        result = self.dao.show_variables(
            'localhost', 'tests/inventory', None
        )
        self.assertIsNotNone(result)
