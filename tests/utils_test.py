# -*- coding: utf-8 -*-

import mock
import unittest

from ansible_toolkit.utils import show_diff


class TestShowDiff(unittest.TestCase):

    """Test case for the ansible_toolkit.utils.show_diff function."""

    @mock.patch('ansible_toolkit.utils.sys.stdout.write', autospec=True)
    def test_no_diff(self, mock_write):

        old = {}
        new = {}

        self.assertIsNone(show_diff(old, new))
        self.assertFalse(mock_write.called)
