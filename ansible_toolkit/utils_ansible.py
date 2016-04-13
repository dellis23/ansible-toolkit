# -*- coding: utf-8 -*-

import tempfile

import ansible.callbacks
from ansible.playbook import PlayBook
import ansible.constants as C
from utils import get_inventory, yellow


SETUP_PLAYBOOK = """
---
- hosts:
    - {host}
  tasks:
    - setup:
"""


class Callbacks(object):

    def __getattr__(self, name):
        def do_nothing(*args, **kwargs):
            return
        return do_nothing


def gather_facts(host, inventory=None, user=None):
    if inventory is None:
        inventory = get_inventory()

    # Gather facts
    try:

        # ... temporary playbook file
        playbook_file = tempfile.NamedTemporaryFile()
        playbook_file.write(SETUP_PLAYBOOK.format(host=host))
        playbook_file.seek(0)

        # ... run setup module
        stats = ansible.callbacks.AggregateStats()
        playbook = PlayBook(
            playbook=playbook_file.name,
            inventory=inventory,
            callbacks=Callbacks(),
            runner_callbacks=Callbacks(),
            remote_user=user or C.DEFAULT_REMOTE_USER,
            stats=stats,
        )
        results = playbook.run()

        # ... notify the user of failures
        for host, result in results.iteritems():
            if result.get('unreachable') or result.get('failures'):
                yellow('Unable to gather facts for host "{}"'.format(host))

    finally:
        playbook_file.close()

    return playbook.SETUP_CACHE
