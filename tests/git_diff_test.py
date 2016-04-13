# -*- coding: utf-8 -*-

import tempfile
import unittest

from ansible_toolkit import git_diff
from ansible_toolkit.exceptions import MalformedGitDiff


VAULT_PASSWORD = "foo"


# Vaulted Files

OLD_FILE_1 = """$ANSIBLE_VAULT;1.1;AES256
35626233663138316665643331653539633239313534376130633265353137313531656664613539
6466346666333332636231356362323834616462323161610a613533363462663730366462633466
36303466376432323137383661653036663338343830666264343562643833313931616165653463
6637633063376664360a643964336134383034343665383730623064353338366436326135366265
3038"""

OLD_FILE_1_DECRYPTED = """foo
"""

NEW_FILE_1 = """$ANSIBLE_VAULT;1.1;AES256
39373663313137383662393466386133396438366235323234336365623535363133353631366566
3565616539353938343863633635626334636532393936390a353430663164393034616161356237
34386335363662623266646637653135613337666636323834313764303766306131663334336436
6633623031353931640a626366353232613963303939303130313132666437346163363535663265
6535"""

NEW_FILE_1_DECRYPTED = """bar
"""


# Git Diff Output

DIFF_HEAD_1 = """diff --git a/group_vars/foo b/group_vars/foo
index c09080b..0d803bb 100644
--- a/group_vars/foo
+++ b/group_vars/foo
"""

SAMPLE_DIFF = DIFF_HEAD_1

SAMPLE_DIFF += """@@ -1,32 +1,33 @@
ANSIBLE_VAULT;1.1;AES256"""

SAMPLE_DIFF += ''.join('\n-' + i for i in OLD_FILE_1.split('\n')[1:])
SAMPLE_DIFF += ''.join('\n+' + i for i in NEW_FILE_1.split('\n')[1:])

# ... another section to make sure we can handle multiple parts

SAMPLE_DIFF += """
diff --git a/group_vars/bar b/group_vars/bar
index 6b9eef7..eb9fb09 100644
--- a/group_vars/bar
+++ b/group_vars/bar
@@ -1,22 +1,23 @@
 $ANSIBLE_VAULT;1.1;AES256
-32346330646639326335373939383634656365376531353531306238616239626265313963613561
-61393637373834646566353739393762306436393234636438323434626666366136
+65393432336536653066303736336632356364306533643131656461316332353138316239336137
+3038396139303439356236343161396331353332326232626566"""

DELETED_FILE_DIFF = """
diff --git a/foo b/foo
deleted file mode 100644
index 257cc56..0000000
--- a/foo
+++ /dev/null
@@ -1 +0,0 @@
-foo"""

ADDED_FILE_DIFF = """
diff --git a/bar b/bar
new file mode 100644
index 0000000..5716ca5
--- /dev/null
+++ b/bar
@@ -0,0 +1 @@
+bar"""


class TestGitDiff(unittest.TestCase):

    def test_get_parts(self):
        parts = git_diff.get_parts(SAMPLE_DIFF)
        self.assertEqual(len(parts), 2)

    def test_get_old_sha(self):
        parts = git_diff.get_parts(SAMPLE_DIFF)
        old_sha = git_diff.get_old_sha(parts[0])
        self.assertEqual(old_sha, 'c09080b')

    def test_get_old_filename(self):
        parts = git_diff.get_parts(SAMPLE_DIFF)
        old_filename = git_diff.get_old_filename(parts[0])
        self.assertEqual(old_filename, 'group_vars/foo')

    def test_get_old_filename_for_added_file(self):
        parts = git_diff.get_parts(ADDED_FILE_DIFF)
        old_filename = git_diff.get_old_filename(parts[0])
        self.assertEqual(old_filename, '/dev/null')

    def test_missing_old_filename_raises_exception(self):
        self.assertRaises(MalformedGitDiff, git_diff.get_old_filename, '')

    def test_get_new_filename(self):
        parts = git_diff.get_parts(SAMPLE_DIFF)
        new_filename = git_diff.get_new_filename(parts[0])
        self.assertEqual(new_filename, 'group_vars/foo')

    def test_get_new_filename_for_deleted_file(self):
        parts = git_diff.get_parts(DELETED_FILE_DIFF)
        new_filename = git_diff.get_new_filename(parts[0])
        self.assertEqual(new_filename, '/dev/null')

    def test_missing_new_filename_raises_exception(self):
        self.assertRaises(MalformedGitDiff, git_diff.get_new_filename, '')

    def test_decrypt_diff(self):

        # Monkey-patch
        _get_old_contents = git_diff.get_old_contents

        def get_old_contents(*args):  # noqa
            return OLD_FILE_1
        git_diff.get_old_contents = get_old_contents
        _get_new_contents = git_diff.get_new_contents

        def get_new_contents(*args):  # noqa
            return NEW_FILE_1
        git_diff.get_new_contents = get_new_contents

        # Test decryption
        try:

            # ... create temporary vault file
            f = tempfile.NamedTemporaryFile()
            f.write(VAULT_PASSWORD)
            f.seek(0)

            # ... decrypt the diff
            parts = git_diff.get_parts(SAMPLE_DIFF)
            old, new = git_diff.decrypt_diff(
                parts[0], password_file=f.name)
            self.assertEqual(old, OLD_FILE_1_DECRYPTED)
            self.assertEqual(new, NEW_FILE_1_DECRYPTED)

        # Restore monkey-patched functions
        finally:
            git_diff.get_old_contents = _get_old_contents
            git_diff.get_new_contents = _get_new_contents

    def test_get_head(self):
        parts = git_diff.get_parts(SAMPLE_DIFF)
        head = git_diff.get_head(parts[0])
        self.assertEqual(head, DIFF_HEAD_1)


if __name__ == '__main__':
    unittest.main()
