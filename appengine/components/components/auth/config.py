# Copyright 2014 The Swarming Authors. All rights reserved.
# Use of this source code is governed by the Apache v2.0 license that can be
# found in the LICENSE file.

"""Auth component configuration hooks.

Application that use 'auth' component can override settings defined here by
adding the following lines to appengine_config.py:

  components_auth_UI_APP_NAME = 'My service name'

Code flow when this is used:
  * GAE app starts and loads a module with main WSGI app.
  * This module import 'components.auth'.
  * components.auth imports components.auth.config (thus executing code here).
  * lib_config.register below imports appengine_config.py.
  * Later when code path hits auth-related code, ensure_configured is called.
  * ensure_configured calls handler.configure and auth.ui.configure.
  * Fin.
"""

import threading

from google.appengine.api import lib_config

# Used in ensure_configured.
_config_lock = threading.Lock()
_config_called = False


# Read the configuration. It would be applied later in 'ensure_configured'.
_config = lib_config.register(
    'components_auth',
    {
      # Title of the service to show in UI.
      'UI_APP_NAME': 'Auth',
      # True if application is calling 'configure_ui' manually.
      'UI_CUSTOM_CONFIG': False,
    })


def ensure_configured():
  """Applies component configuration.

  Called lazily when auth component is used for a first time.
  """
  global _config_called

  # Import lazily to avoid module reference cycle.
  from components import utils
  from . import handler
  from .ui import ui

  with _config_lock:
    if not _config_called:
      authenticators = []
      # OAuth mocks on dev server always return useless values, don't use it.
      if not utils.is_local_dev_server():
        authenticators.append(handler.oauth_authentication)
      authenticators.extend([
        handler.cookie_authentication,
        handler.service_to_service_authentication,
      ])
      handler.configure(authenticators)
      # Customize auth UI to show where it's running.
      if not _config.UI_CUSTOM_CONFIG:
        ui.configure_ui(_config.UI_APP_NAME)
      # Mark as successfully completed.
      _config_called = True
