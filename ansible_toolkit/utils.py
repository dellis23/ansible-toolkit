import ConfigParser
import errno
import os

from ansible.inventory import Inventory
from ansible.utils import read_vault_file


config = ConfigParser.ConfigParser()

config.read([os.path.expanduser('~/.atk')])


# Terminal Colors

RED = '\033[31m'
GREEN = '\033[32m'
CYAN = '\033[36m'
INTENSE = '\033[1m'
ENDC = '\033[0m'


def green(text):
    print GREEN + text + ENDC


def red(text):
    print RED + text + ENDC


def cyan(text):
    print CYAN + text + ENDC


def intense(text):
    print INTENSE + text + ENDC


# Vault Password

def get_vault_password(password_file=None):
    if password_file is None:
        try:
            password_file = config.get('vault', 'password_file')
        except ConfigParser.NoSectionError:
            return None
    return read_vault_file(password_file)


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
