#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pip.download

from pip.req import parse_requirements

from setuptools import setup

setup(name='ansible-toolkit',
      version='1.3.2',
      description='The missing Ansible tools',
      url='http://github.com/dellis23/ansible-toolkit',
      author='Daniel Ellis',
      author_email='ellisd23@gmail.com',
      license='GPLv3',
      install_requires=[
            str(pkg.req) for pkg in parse_requirements(
                  'requirements.txt',
                  session=pip.download.PipSession())],
      tests_require=[
          str(pkg.req) for pkg in parse_requirements(
                  'test-requirements.txt',
                  session=pip.download.PipSession())],
      packages=['ansible_toolkit'],
      scripts=[
          'bin/atk-git-diff',
          'bin/atk-show-vars',
          'bin/atk-show-template',
          'bin/atk-vault',
      ])
