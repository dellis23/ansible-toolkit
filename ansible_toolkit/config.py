# -*- coding: utf-8 -*-

import ConfigParser
import os.path

config_data = ConfigParser.ConfigParser()
config_data.read([os.path.expanduser('~/.atk')])
