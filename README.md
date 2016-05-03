# Ansible Toolkit

[![Build Status](https://travis-ci.org/dellis23/ansible-toolkit.svg?branch=master)](https://travis-ci.org/dellis23/ansible-toolkit)
[![Code Health](https://landscape.io/github/dellis23/ansible-toolkit/master/landscape.svg?style=flat)](https://landscape.io/github/dellis23/ansible-toolkit/master)
[![Coverage Status](https://coveralls.io/repos/github/dellis23/ansible-toolkit/badge.svg?branch=master)](https://coveralls.io/r/dellis23/ansible-toolkit)
[![Requirements Status](https://requires.io/github/dellis23/ansible-toolkit/requirements.svg?branch=master)](https://requires.io/github/dellis23/ansible-toolkit/requirements/?branch=master)


## Description

Ansible is a neat infrastructure management tool, but it sometimes feels
like the only way to to find out what's going to happen when you run things
is to... run them.  That's time consuming and potentially dangerous.

**Ansible Toolkit** hopes to solve that by providing some simple additional
visibility tools. 

## Setup

Just pip install it.

    pip install ansible-toolkit

### Configuration ###

If you are using vault files, you will need to set up a config file in `~/.atk`
pointing to your vault password file:

    [vault]
    password_file = ~/.vault

By default, inventory will be read from the path `inventory`, relative to the
directory an Ansible Toolkit command is run from.  To override:

    [inventory]
    path = /home/foo/inventory

### Optional Arguments ###

If you have multiple Ansible inventories or password files, or for whatever reason do not wish to set up a configuration file, the configuration can be optionally passed on the command line:

    -i, --inventory
    -p, --vault-password-file

## Tools

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

#### Optional Arguments ####

 * `--no-gather-facts` - disable fact gathering on host

### atk-vault ###

With a large amount of vaulted ansible files, encrypting can take
a while and grepping can be tedious.

`atk-vault` allows you to mass decrypt your vault files, do some
work, and re-encrypt when done.  Encrypted files that are changed
while the vault is open will be updated upon re-encryption.

To open the vault:

	$ atk-vault open

To close the vault:

	$ atk-vault close

When the vault is opened, the original encrypted files will be stored in `.atk-vault`.  You may wish to add this to your version
control system's ignore file.

It's important that the vault always be opened and closed from the
base directory of your ansible project.  Newer versions may attempt
to detect and force this by default.

### atk-git-diff ###

Doing a `git diff` on encrypted files produces some pretty useless output.  
`atk-git-diff` will detect changes via `git diff`, unencrypt the before and 
after, and show the difference.

This:

   ![Encrypted git diff output](https://github.com/dellis23/ansible-toolkit/blob/master/img/git-diff-encrypted.png)

Becomes:

   ![Unencrypted git diff output](https://github.com/dellis23/ansible-toolkit/blob/master/img/git-diff-unencrypted.png)


## Contributing

There's probably a few things here that are too narrow and will only work
on my team's platform / setup.  If you run into any obvious problems / 
limitations please create an issue.  If people start using this, I'll be happy
to make it work for more environments.


## Changelog

Please visit the [Releases page](https://github.com/dellis23/ansible-toolkit/releases).

