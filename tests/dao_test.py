# -*- coding: utf-8 -*-

import ansible
import ansible_toolkit.dao
import unittest


class InitTestCase(unittest.TestCase):

    """
    Test case for the
    ansible_toolkit.dao.AnsibleDao.__init__() function.
    """

    def test(self):
        dao = ansible_toolkit.dao.create_dao()
        self.assertEqual(ansible.__version__, dao.version)


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
