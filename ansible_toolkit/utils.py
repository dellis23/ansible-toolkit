# -*- coding: utf-8 -*-

import ConfigParser
import errno
import os
import sys

from ansible.inventory import Inventory

from . import DaoImpl

config = ConfigParser.ConfigParser()

config.read([os.path.expanduser('~/.atk')])


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


# Vault Password

def get_vault_password(password_file=None):
    if password_file is None:
        try:
            password_file = config.get('vault', 'password_file')
        except ConfigParser.NoSectionError:
            return None
    return DaoImpl.read_vault_file(password_file)


# Inventory

def get_inventory(inventory_path=None, vault_password_path=None):
    if inventory_path is None:
        try:
            inventory_path = os.path.expanduser(
                config.get('inventory', 'path'))
        except ConfigParser.NoSectionError:
            inventory_path = 'inventory'
    vault_password = get_vault_password(vault_password_path)
    return Inventory(inventory_path, vault_password=vault_password)


# Filesystem Tools

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
