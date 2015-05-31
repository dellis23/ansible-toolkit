import ConfigParser
import os


# Terminal Colors

GREEN = '\033[92m'
RED = '\033[91m'
ENDC = '\033[0m'


def green(text):
    print GREEN + text + ENDC


def red(text):
    print RED + text + ENDC


# Vault Password

config = ConfigParser.ConfigParser()


def get_vault_password():
    config.read(['site.cfg', os.path.expanduser('~/.atk')])
    try:
        password_file = config.get('vault', 'password_file')
        with open(password_file, 'rb') as f:
            return f.read()
    except ConfigParser.NoSectionError:
        return None
