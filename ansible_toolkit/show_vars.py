from ansible.runner import Runner
from ansible.utils import combine_vars, template

from utils import green, red, get_vault_password, get_inventory


def show_diff(old, new):
    for k, v in new.iteritems():
        if k in old.keys() and v == old[k]:
            continue
        if k in old.keys() and v != old[k]:
            red(" - ['{}'] = {}".format(k, old[k]))
        green(" + ['{}'] = {}".format(k, v))


def get_inject_vars(self, host):

    host_variables = self.inventory.get_variables(
        host, vault_password=self.vault_pass)
    ansible_host = self.inventory.get_host(host)

    # Keep track of variables in the order they will be merged
    to_merge = [
        ('Default Variables', self.default_vars),
    ]

    # Group variables
    groups = ansible_host.get_groups()
    for group in sorted(groups, key=lambda g: g.depth):
        to_merge.append(
            ("Group Variables ({})".format(group.name), group.get_variables())
        )

    combined_cache = self.get_combined_cache()

    # use combined_cache and host_variables to template the module_vars
    # we update the inject variables with the data we're about to template
    # since some of the variables we'll be replacing may be contained there too
    module_vars_inject = combine_vars(
        host_variables, combined_cache.get(host, {}))
    module_vars_inject = combine_vars(
        self.module_vars, module_vars_inject)
    module_vars = template.template(
        self.basedir, self.module_vars, module_vars_inject)

    inject = {}
    to_merge.extend([
        ('Host Variables', ansible_host.vars),
        ('Setup Cache', self.setup_cache.get(host, {})),
        ('Play Variables', self.play_vars),
        ('Play File Variables', self.play_file_vars),
        ('Role Variables', self.role_vars),
        ('Module Variables', module_vars),
        ('Variables Cache', self.vars_cache.get(host, {})),
        ('Role Parameters', self.role_params),
        ('Extra Variables', self.extra_vars),
    ])
    for name, value in to_merge:
        old_inject = inject
        inject = combine_vars(inject, value)
        print name
        show_diff(old_inject, inject)

    return inject


def show_vars(host, inventory_file=None, password_file=None):
    inventory = get_inventory(inventory_file, password_file)
    Runner.get_inject_vars = get_inject_vars
    runner = Runner(inventory=inventory)
    runner.get_inject_vars(host)
