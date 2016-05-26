# -*- coding: utf-8 -*-

import ansible_toolkit
import ConfigParser
import errno
import os
import sys

# Terminal Colors

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
INTENSE = '\033[1m'
ENDC = '\033[0m'


def green(text):
    sys.stdout.write('%s%s%s\n' % (GREEN, text, ENDC))


def red(text):
    sys.stdout.write('%s%s%s\n' % (RED, text, ENDC))


def yellow(text):
    sys.stdout.write('%s%s%s\n' % (YELLOW, text, ENDC))


def cyan(text):
    sys.stdout.write('%s%s%s\n' % (CYAN, text, ENDC))


def intense(text):
    sys.stdout.write('%s%s%s\n' % (INTENSE, text, ENDC))


# Filesystem Tools

def get_files(path):
    """
    Returns a recursive list of all non-hidden files in and below the current
    directory.
    """
    return_files = []
    for root, dirs, files in os.walk(path):

        # Skip hidden files
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']

        for filename in files:
            return_files.append(os.path.join(root, filename))
    return return_files


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def split_path(path):
    """
        "/tmp/test"

    Becomes:

        ("/", "tmp", "test")
    """
    parts = []
    path, tail = os.path.split(path)
    while path and tail:
        parts.append(tail)
        path, tail = os.path.split(path)
    parts.append(os.path.join(path, tail))
    return map(os.path.normpath, parts)[::-1]


# Other

def get_vault_password_file():
    """
    Returns the atk configured location for the Ansible vault password file.

    :return: the atk configured location for the Ansible vault password file.
    """
    try:
        return \
            ansible_toolkit.config.get('vault', 'password_file')
    except ConfigParser.NoSectionError:
        pass

    return None


def show_diff(old, new):
    for k, v in new.iteritems():
        if k in old.keys() and v == old[k]:
            continue
        if k in old.keys() and v != old[k]:
            red(" - ['{}'] = {}".format(k, old[k]))
        green(" + ['{}'] = {}".format(k, v))
