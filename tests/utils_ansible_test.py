# -*- coding: utf-8 -*-

import mock
import unittest


class CallbackTestCase(unittest.TestCase):

    """
    Test case for the
    ansible_toolkit.utils_ansible.Callbacks class.
    """

    @mock.patch(
        'ansible_toolkit.utils_ansible.ansible', autospec=True)
    def test(self, _):
        """Test ansible_toolkit.utils_ansible.Callbacks.__getattr__()."""
        from ansible_toolkit.utils_ansible import Callbacks

        instance = Callbacks()

        self.assertIsNone(instance.noattribute())
