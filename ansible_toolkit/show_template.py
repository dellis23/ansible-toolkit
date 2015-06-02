from ansible.runner import Runner
from ansible.utils.template import template_from_file

from utils import get_inventory


def show_template(host, path):
    inventory = get_inventory()
    runner = Runner(inventory=inventory)
    host_vars = runner.get_inject_vars(host)
    print template_from_file('.', path, host_vars)
