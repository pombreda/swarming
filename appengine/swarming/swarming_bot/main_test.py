#!/usr/bin/env python
# Copyright 2014 The Swarming Authors. All rights reserved.
# Use of this source code is governed by the Apache v2.0 license that can be
# found in the LICENSE file.

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

BOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BOT_DIR)
sys.path.insert(0, ROOT_DIR)

import test_env

test_env.setup_test_env()

from depot_tools import auto_stub
from server import bot_archive
import bot_main


class MainTest(auto_stub.TestCase):
  def setUp(self):
    with open(os.path.join(BOT_DIR, 'bot_config.py'), 'rb') as f:
      bot_config_content = f.read()
    zip_content = bot_archive.get_swarming_bot_zip(
        BOT_DIR, 'http://localhost', {'bot_config.py': bot_config_content})
    self.tmpdir = tempfile.mkdtemp(prefix='main')
    self.zip_file = os.path.join(self.tmpdir, 'swarming_bot.zip')
    with open(self.zip_file, 'wb') as f:
      f.write(zip_content)

  def tearDown(self):
    shutil.rmtree(self.tmpdir)

  def test_attributes(self):
    actual = json.loads(subprocess.check_output(
        [sys.executable, self.zip_file, 'attributes']))
    expected = bot_main.get_attributes()
    for key in ('cwd', 'disks', 'running_time', 'started_ts'):
      del actual['state'][key]
      del expected['state'][key]
    del actual['version']
    del expected['version']
    self.assertEqual(expected, actual)

  def test_version(self):
    version = subprocess.check_output(
        [sys.executable, self.zip_file, 'version'])
    lines = version.strip().split()
    self.assertEqual(2, len(lines), lines)
    self.assertEqual('0.3', lines[0])
    self.assertTrue(re.match(r'^[0-9a-f]{40}$', lines[1]), lines[1])


if __name__ == '__main__':
  if '-v' in sys.argv:
    unittest.TestCase.maxDiff = None
  unittest.main()
