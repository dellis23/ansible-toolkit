import ConfigParser
import os

from ansible.inventory import Inventory


config = ConfigParser.ConfigParser()

config.read([os.path.expanduser('~/.atk')])


# Terminal Colors

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'


def green(text):
    print GREEN + text + ENDC


def red(text):
    print RED + text + ENDC


# Vault Password

def get_vault_password():
    try:
        password_file = config.get('vault', 'password_file')
        with open(password_file, 'rb') as f:
            return f.read()
    except ConfigParser.NoSectionError:
        return None


# Inventory

def get_inventory():
    try:
        inventory_path = config.get('inventory', 'path')
    except ConfigParser.NoSectionError:
        inventory_path = 'inventory'
    return Inventory(inventory_path, vault_password=get_vault_password())
