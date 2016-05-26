# -*- coding: utf-8 -*-

import ansible_toolkit.dao
import unittest


class ShowVariablesTestCase(unittest.TestCase):

    """Test case for the ansible_toolkit.dao.show_variables() function."""

    def setUp(self):
        self.dao = ansible_toolkit.dao.create_dao()

    def test(self):
        """
        """

        result = self.dao.show_variables(
            'localhost', 'tests/inventory', None
        )
        self.assertIsNotNone(result)
