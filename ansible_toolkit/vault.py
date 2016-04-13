# -*- coding: utf-8 -*-

import hashlib
import os

from utils import get_vault_password, mkdir_p, split_path, get_files

from . import DaoImpl

ATK_VAULT = '.atk-vault'

VaultLib = DaoImpl.get_vault_lib()


def backup(path, password_file=None):
    """
    Replaces the contents of a file with its decrypted counterpart, storing the
    original encrypted version and a hash of the file contents for later
    retrieval.
    """
    vault = VaultLib(get_vault_password(password_file))
    with open(path, 'r') as f:
        encrypted_data = f.read()

        # Normally we'd just try and catch the exception, but the
        # exception raised here is not very specific (just
        # `AnsibleError`), so this feels safer to avoid suppressing
        # other things that might go wrong.
        if vault.is_encrypted(encrypted_data):
            decrypted_data = vault.decrypt(encrypted_data)

            # Create atk vault files
            atk_path = os.path.join(ATK_VAULT, path)
            mkdir_p(atk_path)
            # ... encrypted
            with open(os.path.join(atk_path, 'encrypted'), 'wb') as f:
                f.write(encrypted_data)
            # ... hash
            with open(os.path.join(atk_path, 'hash'), 'wb') as f:
                f.write(hashlib.sha1(decrypted_data).hexdigest())

            # Replace encrypted file with decrypted one
            with open(path, 'wb') as f:
                f.write(decrypted_data)


def backup_all(password_file=None):
    for file_ in get_files('.'):
        backup(file_, password_file)


def restore(path, password_file=None):
    """
    Retrieves a file from the atk vault and restores it to its original
    location, re-encrypting it if it has changed.

    :param path: path to original file
    """
    vault = VaultLib(get_vault_password(password_file))
    atk_path = os.path.join(ATK_VAULT, path)

    # Load stored data
    with open(os.path.join(atk_path, 'encrypted'), 'rb') as f:
        old_data = f.read()
    with open(os.path.join(atk_path, 'hash'), 'rb') as f:
        old_hash = f.read()

    # Load new data
    with open(path, 'rb') as f:
        new_data = f.read()
        new_hash = hashlib.sha1(new_data).hexdigest()

    # Determine whether to re-encrypt
    if old_hash != new_hash:
        new_data = vault.encrypt(new_data)
    else:
        new_data = old_data

    # Update file
    with open(path, 'wb') as f:
        f.write(new_data)

    # Clean atk vault
    os.remove(os.path.join(atk_path, 'encrypted'))
    os.remove(os.path.join(atk_path, 'hash'))


def restore_all(password_file=None):
    for file_ in get_files(ATK_VAULT):
        if os.path.basename(file_) == 'encrypted':

            # Get the path without the atk vault base and encrypted filename
            original_path = os.path.join(*split_path(file_)[1:-1])
            restore(original_path, password_file)
