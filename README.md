Ansible Toolkit
===============

Setup
-----

    pip install ansible-toolkit

If you are using vault files, you will need to set up a config file in `~/.atk`
pointing to your vault password file:

    [vault]
    password_file = ~/.vault

By default, inventory will be read from the path `inventory`, relative to the
directory an Ansible Toolkit command is run from.  To override:

    [inventory]
    path = /home/foo/inventory

Usage
-----

### atk-show-vars ###

You can display a list of all variables affecting a host, with a diff of each 
when they are overridden by a subgroup.

    $ atk-show-vars host
    Group Variables (all)
     + ['foo'] = 3
    Group Variables (sub-group)
     - ['foo'] = 3
     + ['foo'] = 5

### atk-show-template ###

You can display what the output of a template will be when applied against a 
host.  For instance, if this were the template:

    template_key = {{ template_var }}

And the value of `template_var` was set to `3` for `host`, the output would be:

    $ atk-show-template host roles/foo/templates/template.j2
    template_key = 3
