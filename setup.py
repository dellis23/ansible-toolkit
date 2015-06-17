from setuptools import setup


setup(name='ansible-toolkit',
      version='1.3.0',
      description='The missing Ansible tools',
      url='http://github.com/dellis23/ansible-toolkit',
      author='Daniel Ellis',
      author_email='ellisd23@gmail.com',
      license='GPLv3',
      install_requires=['ansible'],
      packages=['ansible_toolkit'],
      scripts=[
          'bin/atk-git-diff',
          'bin/atk-show-vars',
          'bin/atk-show-template',
          'bin/atk-vault',
      ])
