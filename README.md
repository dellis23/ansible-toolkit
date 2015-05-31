Ansible Toolkit
===============

Setup
-----

    pip install ansible-toolkit

If you are using vault files, you will need to set up a config file in `~/.atk`
pointing to your vault password file:

    [vault]
    password_file = ~/.vault

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
