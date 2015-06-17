import difflib
from itertools import islice
import re
import subprocess

from ansible.utils.vault import VaultLib

from utils import get_vault_password, green, red, cyan, intense


def get_parts(git_diff_output):
    r = re.compile(r"^diff --git", re.MULTILINE)
    parts = []
    locations = [i.start() for i in r.finditer(git_diff_output)]
    for i, location in enumerate(locations):
        is_last_item = i + 1 == len(locations)
        next_location = None if is_last_item else locations[i + 1]
        parts.append(git_diff_output[location:next_location])
    return parts


def get_old_sha(diff_part):
    """
    Returns the SHA for the original file that was changed in a diff part.
    """
    r = re.compile(r'index ([a-fA-F\d]*)')
    return r.search(diff_part).groups()[0]


def get_old_filename(diff_part):
    """
    Returns the filename for the original file that was changed in a diff part.
    """
    r = re.compile(r'^--- a/(.*)', re.MULTILINE)
    return r.search(diff_part).groups()[0]


def get_old_contents(sha, filename):
    return subprocess.check_output(['git', 'show', sha, '--', filename])


def get_new_filename(diff_part):
    """
    Returns the filename for the updated file in a diff part.
    """
    r = re.compile(r'^\+\+\+ b/(.*)', re.MULTILINE)
    return r.search(diff_part).groups()[0]


def get_new_contents(filename):
    with open(filename, 'rb') as f:
        return f.read()


def get_head(diff_part):
    """
    Returns the pre-content, non-chunk headers of a diff part.

    E.g.

        diff --git a/group_vars/foo b/group_vars/foo
        index 6b9eef7..eb9fb09 100644
        --- a/group_vars/foo
        +++ b/group_vars/foo
    """
    return '\n'.join(diff_part.split('\n')[:4]) + '\n'


def get_contents(diff_part):
    """
    Returns a tuple of old content and new content.
    """
    old_sha = get_old_sha(diff_part)
    old_filename = get_old_filename(diff_part)
    old_contents = get_old_contents(old_sha, old_filename)
    new_filename = get_new_filename(diff_part)
    new_contents = get_new_contents(new_filename)
    return old_contents, new_contents


def decrypt_diff(diff_part, password_file=None):
    """
    Diff part is a string in the format:

        diff --git a/group_vars/foo b/group_vars/foo
        index c09080b..0d803bb 100644
        --- a/group_vars/foo
        +++ b/group_vars/foo
        @@ -1,32 +1,33 @@
         $ANSIBLE_VAULT;1.1;AES256
        -61316662363730313230626432303662316330323064373866616436623565613033396539366263
        -383632656663356364656531653039333965
        +30393563383639396563623339383936613866326332383162306532653239636166633162323236
        +62376161626137626133

    Returns a tuple of decrypted old contents and decrypted new contents.
    """
    vault = VaultLib(get_vault_password(password_file))
    old_contents, new_contents = get_contents(diff_part)
    if vault.is_encrypted(old_contents):
        old_contents = vault.decrypt(old_contents)
    if vault.is_encrypted(new_contents):
        new_contents = vault.decrypt(new_contents)
    return old_contents, new_contents


def show_unencrypted_diff(diff_part, password_file=None):
    intense(get_head(diff_part).strip())
    old, new = decrypt_diff(diff_part, password_file)
    diff = difflib.unified_diff(old.split('\n'), new.split('\n'), lineterm='')
    # ... we'll take the git filenames from git's diff output rather than
    # ... difflib
    for line in islice(diff, 2, None):
        if line.startswith('-'):
            red(line)
        elif line.startswith('+'):
            green(line)
        elif line.startswith('@@'):
            cyan(line)
        else:
            print line


def show_unencrypted_diffs(git_diff_output, password_file=None):
    parts = get_parts(git_diff_output)
    for part in parts:
        show_unencrypted_diff(part, password_file)
