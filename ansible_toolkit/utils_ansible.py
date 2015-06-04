import tempfile

import ansible.callbacks
from ansible.playbook import PlayBook

from utils import get_inventory


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


def gather_facts(host, inventory=None):
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
        # callbacks = ansible.callbacks.PlaybookCallbacks(verbose=VERBOSITY)
        # runner_callbacks = ansible.callbacks.PlaybookRunnerCallbacks(
        #     stats, verbose=VERBOSITY)
        playbook = PlayBook(
            playbook=playbook_file.name,
            inventory=inventory,
            callbacks=Callbacks(),
            runner_callbacks=Callbacks(),
            stats=stats,
        )
        playbook.run()

    finally:
        playbook_file.close()

    return playbook.SETUP_CACHE
